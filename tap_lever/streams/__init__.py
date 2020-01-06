from tap_lever.streams.applications import (
    CandidateApplicationsStream,
    OpportunityApplicationsStream,
)
from tap_lever.streams.archive_reasons import ArchiveReasonsStream
from tap_lever.streams.candidates import CandidateStream
from tap_lever.streams.offers import CandidateOffersStream, OpportunityOffersStream
from tap_lever.streams.opportunities import OpportunityStream
from tap_lever.streams.postings import PostingsStream
from tap_lever.streams.referrals import (
    CandidateReferralsStream,
    OpportunityReferralsStream,
)
from tap_lever.streams.requisitions import RequisitionStream
from tap_lever.streams.resumes import CandidateResumesStream, OpportunityResumesStream
from tap_lever.streams.sources import SourcesStream
from tap_lever.streams.stages import StagesStream
from tap_lever.streams.users import UsersStream

AVAILABLE_STREAMS = [
    CandidateStream,  # must sync first to fill CACHE
    OpportunityStream,  # must sync first to fill CACHE
    ArchiveReasonsStream,
    CandidateApplicationsStream,
    CandidateOffersStream,
    CandidateReferralsStream,
    CandidateResumesStream,
    OpportunityApplicationsStream,
    OpportunityOffersStream,
    OpportunityReferralsStream,
    OpportunityResumesStream,
    PostingsStream,
    RequisitionStream,
    SourcesStream,
    StagesStream,
    UsersStream,
]

__all__ = [
    "CandidateStream",
    "OpportunityStream",
    "ArchiveReasonsStream",
    "CandidateApplicationsStream",
    "CandidateOffersStream",
    "CandidateReferralsStream",
    "CandidateResumesStream",
    "OpportunityApplicationsStream",
    "OpportunityOffersStream",
    "OpportunityReferralsStream",
    "OpportunityResumesStream",
    "PostingsStream",
    "RequisitionStream",
    "SourcesStream",
    "StagesStream",
    "UsersStream",
]
