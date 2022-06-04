# import standard modules
from __future__ import annotations
import logging
from uuid import UUID
from typing import Optional, List, Any


# import third party modules
from pydantic import BaseModel, validator


class Context(BaseModel):
    tenantId: str
    casefileId: str
    timestamp: str
    eventType: str
    userId: str
    valid: bool = True
    userRole: Optional[str] = None
    nodeId: Optional[str] = None

    @validator('tenantId', 'casefileId', 'nodeId')
    def must_be_uuid(cls, uuid: str):
        try:
            UUID(uuid)
            return uuid
        except ValueError:
            logging.log(f"ValidationError: in Context expected uuid got {type(uuid)}")


class MaskingBody(BaseModel):
    queryType: str
    query: List[str]
    tableId: List[str]
    groupId: List[str]

    @validator('tableId', 'groupId')
    def must_be_list_of_uuid(cls, uuid_list: list) -> list:
        assert type(uuid_list) == list, "list object expected"
        result = list()
        for uuid in uuid_list:
            try:
                UUID(uuid)
                result.append(uuid)
            except ValueError:
                logging.error(f"ValidationError: in MaskingBody expected List[uuid] got {type(uuid)}")
                result.append("00000000-0000-0000-0000-000000000000")
        return result


class QueryBody(BaseModel):
    queryType: str
    query: List[str]
    tableId: List[str]
    executedQuery: Optional[List[str]]
    groupId: Optional[List[str]]
    followEvent: Optional[QueryBody]

    @validator('queryType')
    def valid_query_type(cls, query_type: str) -> str:
        available_types = ["sqlQuery", "columnQuery", "textQuery"]
        if query_type not in available_types:
            logging.error(f"ValidationError: in QueryBody expected {available_types} got {query_type}")
            return ""
        else:
            return query_type

    @validator('tableId')
    def must_be_list_of_uuid(cls, uuid_list: list) -> list:
        assert type(uuid_list) == list, "list object expected"
        result = list()
        for uuid in uuid_list:
            try:
                UUID(uuid)
                result.append(uuid)
            except ValueError:
                logging.error(f"ValidationError: in QueryBody expected List[uuid] got {type(uuid)}")
                result.append("00000000-0000-0000-0000-000000000000")
        return result


class CaseFileBody(BaseModel):
    queryType: str
    query: List[str]
    tableSchema: List[dict]
    tableData: List[dict]
    executedQuery: Optional[List[str]]


class MaskingEvent(BaseModel):
    context: Context
    body: MaskingBody


class QueryEvent(BaseModel):
    context: Context
    body: QueryBody


class CaseFileEvent(BaseModel):
    context: Context
    body: CaseFileBody
