from tap_lever.streams.base import TimeRangeStream
from tap_lever.streams import cache as stream_cache

import singer

LOGGER = singer.get_logger()  # noqa


class CandidateStream(TimeRangeStream):
    API_METHOD = 'GET'
    TABLE = 'candidates'
    KEY_PROPERTIES = ['id']

    CACHE_RESULTS = True

    @property
    def path(self):
        return '/candidates'
