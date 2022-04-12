# import standard modules
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class QueryEvent:
    case: str
    event_type: str  # general, find_columns_first, source_crawl
    query: list  # order: query
    source: list
    groups: list
    follow_query_event: dict


@dataclass(frozen=True, order=True)
class SourceSnapshot:
    tenant: str
    source: str
    snapshot: str


@dataclass(frozen=True, order=True)
class MaskingEvent:
    type: str
    query: str
    source: list
    groups: list
