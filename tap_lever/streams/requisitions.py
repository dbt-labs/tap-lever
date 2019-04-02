from tap_lever.streams.base import TimeRangeStream
import tap_lever.streams.cache as stream_cache

import singer

LOGGER = singer.get_logger()  # noqa


class RequisitionStream(TimeRangeStream):
    API_METHOD = 'GET'
    TABLE = 'requisitions'
    KEY_PROPERTIES = ['id']
    RANGE_FIELD = 'created_at'

    @property
    def path(self):
        return '/requisitions'
