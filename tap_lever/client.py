import requests
import singer
import singer.metrics

LOGGER = singer.get_logger()  # noqa


class LeverClient:

    MAX_TRIES = 5

    def __init__(self, config):
        self.config = config

    def make_request(self, url, method, params=None, body=None):
        LOGGER.info("Making {} request to {} ({})".format(method, url, params))

        response = requests.request(
            method,
            url,
            headers={
                'Content-Type': 'application/json'
            },
            auth=(self.config['token'], ''),
            params=params,
            json=body)

        if response.status_code != 200:
            raise RuntimeError(response.text)

        return response.json()

