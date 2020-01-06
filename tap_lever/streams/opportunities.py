import singer
from tap_lever.streams import cache as stream_cache
from tap_lever.streams.base import TimeRangeStream

LOGGER = singer.get_logger()  # noqa


class OpportunityStream(TimeRangeStream):
    API_METHOD = "GET"
    TABLE = "opportunities"
    KEY_PROPERTIES = ["id"]

    CACHE_RESULTS = True

    @property
    def path(self):
        return "/opportunities"
