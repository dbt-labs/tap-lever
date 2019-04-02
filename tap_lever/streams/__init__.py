from tap_lever.streams.candidates import CandidateStream
from tap_lever.streams.referrals import CandidateReferralsStream
from tap_lever.streams.postings import PostingsStream
from tap_lever.streams.requisitions import RequisitionStream
from tap_lever.streams.sources import SourcesStream
from tap_lever.streams.stages import StagesStream

AVAILABLE_STREAMS = [
    CandidateStream,
    CandidateReferralsStream,
    PostingsStream,
    RequisitionStream,
    SourcesStream,
    StagesStream,
]

__all__ = [
    'CandidateStream',
    'CandidateReferralsStream',
    'PostingsStream',
    'RequisitionStream',
    'SourcesStream',
    'StagesStream',
]
