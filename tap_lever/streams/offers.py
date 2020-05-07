import singer
from tap_lever.streams import cache as stream_cache
from tap_lever.streams.base import BaseStream

LOGGER = singer.get_logger()  # noqa


class CandidateOffersStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "candidate_offers"

    @property
    def path(self):
        return "/candidates/{candidate_id}/offers"

    def get_url(self, candidate):
        _path = self.path.format(candidate_id=candidate)
        return "https://api.lever.co/v1{}".format(_path)

    def sync_data(self):
        candidates = stream_cache.get("candidates")
        LOGGER.info("Found {} candidates in cache".format(len(candidates)))

        params = self.get_params(_next=None)
        for i, candidate in enumerate(candidates):
            LOGGER.info(
                "Fetching offers for candidate {} of {}".format(i + 1, len(candidates))
            )
            candidate_id = candidate["id"]
            url = self.get_url(candidate_id)
            resources = self.sync_paginated(url, params)


class OpportunityOffersStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "opportunity_offers"

    @property
    def path(self):
        return "/opportunities/{opportunity_id}/offers"

    def get_url(self, opportunity):
        _path = self.path.format(opportunity_id=opportunity)
        return "https://api.lever.co/v1{}".format(_path)

    # NB: We chose to change this function to NOT call base's
    # sync_paginated since there was a request to add the parent id
    # (opportunityId) to the records, and there was no natural place to do
    # this
    def sync_data(self, opportunity_id):
        params = self.get_params(_next=None)
        url = self.get_url(opportunity_id)
        resources = self.sync_paginated(url, params)

        transformer = singer.Transformer()
        with singer.metrics.record_counter(endpoint=self.TABLE) as counter:
            for page in self.paginate(url, params, opportunity_id):
                self.add_parent_id(page, opportunity_id)
                transformed_data = self.get_stream_data(page, transformer)
                singer.write_records(self.TABLE, transformed_data)
                counter.increment(len(page))
        transformer.log_warning()

    def paginate(self, url, params, opportunity_id):
        _next = True
        page = 1

        while _next is not None:
            result = self.client.make_request(url, self.API_METHOD, params=params)
            _next = result.get('next')

            yield result['data']

            if _next:
                params['offset'] = _next
            LOGGER.info('Synced page {} for {}'.format(page, self.TABLE))
            page += 1


    def add_parent_id(self, data, opportunity_id):
        for rec in data:
            rec['opportunityId'] = opportunity_id
