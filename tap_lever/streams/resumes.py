import singer

from tap_lever.streams import cache as stream_cache
from tap_lever.streams.base import BaseStream

LOGGER = singer.get_logger()  # noqa


class CandidateResumesStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "candidate_resumes"

    @property
    def path(self):
        return "/candidates/{candidate_id}/resumes"

    def get_url(self, candidate):
        _path = self.path.format(candidate_id=candidate)
        return "https://api.lever.co/v1{}".format(_path)

    def sync_data(self):
        candidates = stream_cache.get("candidates")
        LOGGER.info("Found {} candidates in cache".format(len(candidates)))

        for i, candidate in enumerate(candidates):
            LOGGER.info(
                "Fetching resumes for candidate {} of {}".format(i + 1, len(candidates))
            )
            candidate_id = candidate["id"]
            url = self.get_url(candidate_id)
            resources = self.sync_paginated(url)


class OpportunityResumesStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "opportunity_resumes"

    @property
    def path(self):
        return "/opportunities/{opportunity_id}/resumes"

    def get_url(self, opportunity):
        _path = self.path.format(opportunity_id=opportunity)
        return "https://api.lever.co/v1{}".format(_path)

    def sync_data(self):
        opportunities = stream_cache.get("opportunities")
        LOGGER.info("Found {} opportunities in cache".format(len(opportunities)))

        for i, opportunity in enumerate(opportunities):
            LOGGER.info(
                "Fetching resumes for opportunity {} of {}".format(
                    i + 1, len(opportunities)
                )
            )
            opportunity_id = opportunity["id"]
            url = self.get_url(opportunity_id)
            resources = self.sync_paginated(url)
