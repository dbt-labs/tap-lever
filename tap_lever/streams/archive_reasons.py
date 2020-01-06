import singer
from tap_lever.streams.base import BaseStream

LOGGER = singer.get_logger()  # noqa


class ArchiveReasonsStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "archive_reasons"

    @property
    def path(self):
        return "/archive_reasons"
