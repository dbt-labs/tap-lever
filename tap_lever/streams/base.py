import math
import pytz
import singer
import singer.utils
import singer.metrics

from datetime import timedelta, datetime

from tap_lever.streams import cache as stream_cache
from tap_lever.config import get_config_start_date
from tap_lever.state import incorporate, save_state, \
    get_last_record_value_for_table

from tap_framework.streams import BaseStream as base


LOGGER = singer.get_logger()


class BaseStream(base):
    KEY_PROPERTIES = ['id']
    CACHE_RESULTS = False

    def get_url(self):
        return 'https://api.lever.co/v1{}'.format(self.path)

    def get_params(self, _next):
        params = {"limit": 100}
        if _next:
             params["offset"] = _next

        return params

    def sync_data(self):
        table = self.TABLE

        LOGGER.info('Syncing data for {}'.format(table))

        url = self.get_url()
        params = self.get_params(_next=None)
        resources = self.sync_paginated(url, params)

        if self.CACHE_RESULTS:
            stream_cache.add(table, resources)
            LOGGER.info('Added {} {}s to cache'.format(len(resources), table))

        LOGGER.info('Reached end of stream, moving on.')
        save_state(self.state)
        return self.state

    def sync_paginated(self, url, params=None):
        table = self.TABLE
        _next = True
        page = 1

        all_resources = []
        transformer = singer.Transformer(singer.UNIX_MILLISECONDS_INTEGER_DATETIME_PARSING)
        while _next is not None:
            result = self.client.make_request(url, self.API_METHOD, params=params)
            _next = result.get('next')
            data = self.get_stream_data(result['data'], transformer)

            with singer.metrics.record_counter(endpoint=table) as counter:
                singer.write_records(
                    table,
                    data)
                counter.increment(len(data))
                all_resources.extend(data)

            if _next:
                params['offset'] = _next

            LOGGER.info('Synced page {} for {}'.format(page, self.TABLE))
            page += 1
        transformer.log_warning()
        return all_resources

    def get_stream_data(self, result, transformer):
        metadata = {}

        if self.catalog.metadata is not None:
            metadata = singer.metadata.to_map(self.catalog.metadata)

        return [
            transformer.transform(record, self.catalog.schema.to_dict(), metadata)
            for record in result
        ]

class TimeRangeStream(BaseStream):
    RANGE_FIELD = 'updated_at'

    def get_params(self, start, end):
        return {
            self.RANGE_FIELD + '_start': int(start.timestamp() * 1000),
            self.RANGE_FIELD + '_end': int(end.timestamp() * 1000),
            "limit": 100
        }

    def sync_data(self):
        table = self.TABLE

        date = get_last_record_value_for_table(self.state, table)

        if date is None:
            date = get_config_start_date(self.config)

        interval = timedelta(days=7)

        all_resources = []
        while date < datetime.now(pytz.utc):
            res = self.sync_data_for_period(date, interval)
            all_resources.extend(res)
            date = date + interval

        if self.CACHE_RESULTS:
            stream_cache.add(table, all_resources)
            LOGGER.info('Added {} {}s to cache'.format(len(all_resources), table))

        return self.state

    def sync_data_for_period(self, date, interval):
        table = self.TABLE

        updated_after = date
        updated_before = updated_after + interval

        LOGGER.info(
            'Syncing data from {} to {}'.format(
                updated_after.isoformat(),
                updated_before.isoformat()))

        params = self.get_params(updated_after, updated_before)
        url = self.get_url()
        res = self.sync_paginated(url, params)

        self.state = incorporate(self.state,
                                 table,
                                 self.RANGE_FIELD,
                                 date.isoformat())

        save_state(self.state)
        return res
