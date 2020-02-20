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
            try:
                resources = self.sync_paginated(url)
            except RuntimeError as e:
                # There's a bug in the Lever API where a missing resume will result
                # in a ResourceNotFound error instead of returning an empty response
                if "ResourceNotFound" in str(e):
                    LOGGER.info("Candidate %s does not have resumes", candidate_id)
                else:
                    raise

class OpportunityResumesStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "opportunity_resumes"

    @property
    def path(self):
        return "/opportunities/{opportunity_id}/resumes"

    def get_url(self, opportunity):
        _path = self.path.format(opportunity_id=opportunity)
        return "https://api.lever.co/v1{}".format(_path)

    def sync_data(self, opportunity_id):
        url = self.get_url(opportunity_id)
        try:
            resources = self.sync_paginated(url)
        except RuntimeError as e:
            # There's a bug in the Lever API where a missing resume will result
            # in a ResourceNotFound error instead of returning an empty response
            if "ResourceNotFound" in str(e):
                LOGGER.info("Opportunity %s does not have resumes", opportunity_id)
            else:
                raise
