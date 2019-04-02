from tap_lever.streams.base import BaseStream

import singer

LOGGER = singer.get_logger()  # noqa


class PostingsStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'postings'

    @property
    def path(self):
        return '/postings'
