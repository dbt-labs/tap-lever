from tap_lever.streams.base import BaseStream
import singer

LOGGER = singer.get_logger()  # noqa


class SourcesStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'sources'
    KEY_PROPERTIES = ['text']

    @property
    def path(self):
        return '/sources'

