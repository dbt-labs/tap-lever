from tap_lever.streams.base import BaseStream
import singer

LOGGER = singer.get_logger()  # noqa


class StagesStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'stages'
    KEY_PROPERTIES = ['id']

    @property
    def path(self):
        return '/stages'

