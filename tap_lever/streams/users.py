import singer
from tap_lever.streams.base import BaseStream

LOGGER = singer.get_logger()  # noqa


class UsersStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "users"

    @property
    def path(self):
        return "/users"
