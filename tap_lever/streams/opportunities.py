import singer
from tap_lever.streams import cache as stream_cache
from tap_lever.streams.base import TimeRangeStream
from tap_lever.state import incorporate, save_state, \
    get_last_record_value_for_table
from tap_lever.config import get_config_start_date
from datetime import timedelta, datetime
import pytz
from .applications import OpportunityApplicationsStream
from .offers import OpportunityOffersStream
from .referrals import OpportunityReferralsStream
from .resumes import OpportunityResumesStream
LOGGER = singer.get_logger()  # noqa


class OpportunityStream(TimeRangeStream):
    API_METHOD = "GET"
    TABLE = "opportunities"
    KEY_PROPERTIES = ["id"]

    @property
    def path(self):
        return "/opportunities"

    def sync(self, child_streams=None):
        LOGGER.info('Syncing stream {} with {}'
                    .format(self.catalog.tap_stream_id,
                            self.__class__.__name__))

        self.write_schema()

        return self.sync_data(child_streams)

    def sync_paginated(self, url, params=None, child_streams=None):
        table = self.TABLE
        _next = True
        page = 1

        transformer = singer.Transformer()
        applications_stream = OpportunityApplicationsStream(self.config,
                                                            self.state,
                                                            child_streams['opportunity_applications'],
                                                            self.client)
        offers_stream = OpportunityOffersStream(self.config,
                                                self.state,
                                                child_streams['opportunity_offers'],
                                                self.client)
        referrals_stream = OpportunityReferralsStream(self.config,
                                                      self.state,
                                                      child_streams['opportunity_referrals'],
                                                      self.client)
        resumes_stream = OpportunityResumesStream(self.config,
                                                  self.state,
                                                  child_streams['opportunity_resumes'],
                                                  self.client)
        while _next is not None:
            result = self.client.make_request(url, self.API_METHOD, params=params)
            _next = result.get('next')
            data = self.get_stream_data(result['data'], transformer)

            LOGGER.info('Starting Opportunity child stream syncs')
            for opportunity in data:
                opportunity_id = opportunity['id']

                if child_streams.get('opportunity_applications'):
                    applications_stream.sync_data(opportunity_id)

                if child_streams.get('opportunity_offers'):
                    offers_stream.sync_data(opportunity_id)

                if child_streams.get('opportunity_referrals'):
                    referrals_stream.sync_data(opportunity_id)

                if child_streams.get('opportunity_resumes'):
                    resumes_stream.sync_data(opportunity_id)

            LOGGER.info('Finished Opportunity child stream syncs')


            with singer.metrics.record_counter(endpoint=table) as counter:
                singer.write_records(table, data)
                counter.increment(len(data))

            if _next:
                params['offset'] = _next

            LOGGER.info('Synced page {} for {}'.format(page, self.TABLE))
            page += 1

    def sync_data_for_period(self, date, interval, child_streams=None):
        table = self.TABLE

        updated_after = date
        updated_before = updated_after + interval

        LOGGER.info(
            'Syncing data from {} to {}'.format(
                updated_after.isoformat(),
                updated_before.isoformat()))

        params = self.get_params(updated_after, updated_before)
        url = self.get_url()
        self.sync_paginated(url, params, child_streams)

        self.state = incorporate(self.state,
                                 table,
                                 self.RANGE_FIELD,
                                 date.isoformat())

        save_state(self.state)

    def sync_data(self, child_streams=None):
        table = self.TABLE

        date = get_last_record_value_for_table(self.state, table)

        if date is None:
            date = get_config_start_date(self.config)

        interval = timedelta(days=1)

        while date < datetime.now(pytz.utc):
            self.sync_data_for_period(date, interval, child_streams)
            date = date + interval

        return self.state
