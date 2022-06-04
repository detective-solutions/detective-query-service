# import standard modules
import json
import logging
from operator import itemgetter
from typing import Tuple, Any, List

# import third party modules
import pandas as pd

# import project related modules
from detective_query_service.pydataobject.event_type import QueryEvent, Context
from detective_query_service.service.event import subscribe, post_event
from detective_query_service.pydataobject.dgraph_type import DataBaseConfig
from detective_query_service.utils.query import transform_generic_to_specific_selection_query, execute_query


class QueryOperation:

    @classmethod
    def missing_definition_event(cls, requirement_list: list) -> Tuple[str, Any]:
        index_title = ["name", "database schema", "query"]
        indexes = [ix for ix in requirement_list if ix is None]
        data = pd.DataFrame({"error": list(itemgetter(*indexes)(index_title))})
        schema = [{'headerName': "error", 'field': "error", 'sortable': True, 'filter': True}]

        result = {
            "query": "",
            "schema": schema,
            "data": json.loads(data.to_json(orient="records"))
        }

        return "casefiles", result

    @classmethod
    def insert_column_names(cls, config: DataBaseConfig, event: QueryEvent) -> None:
        try:
            schema, data = execute_query(config, event)
            follow_event = event.body.followEvent

            if "error" not in data.columns.tolist():
                follow_event.query = [
                    transform_generic_to_specific_selection_query(
                        follow_event.query[0],
                        data.Column.tolist()
                    )
                ]

                logging.info(f"find_columns_first_event for {event.context.casefileId} executed")
                post_event("kafka_masking_response", {"body": follow_event, "context": event.context})

            else:
                logging.info(f"query was not successful {event.context.casefileId}")
                cls.construct_casefile_response(
                    query_type=event.body.queryType,
                    query=event.body.query,
                    schema=schema,
                    data=json.loads(data.to_json(orient="records")),
                    context=event.context
                )

        except Exception as e:
            logging.error(f"insert_column_names could not be executed with context {event.context.dict()} with {e}")

    @classmethod
    def general_query_event(cls, config: DataBaseConfig, event: QueryEvent) -> None:
        schema, data = execute_query(config, event)
        cls.construct_casefile_response(
            query_type=event.body.queryType,
            query=event.body.query,
            schema=schema,
            data=json.loads(data.to_json(orient="records")),
            context=event.context
        )

    @classmethod
    def construct_casefile_response(cls, query_type: str, query: str, schema: List[dict],
                                    data: List[dict], context: Context) -> None:

        result = {
            "queryType": query_type,
            "query": query,
            "tableSchema": schema,
            "tableData": data
        }

        post_event("kafka_casefile_response", {"body": result, "context": context})

    @classmethod
    def run_query(cls, request: dict) -> None:
        event = request.get("event")
        config = request.get("config")
        query_type = event.body.queryType

        for db_conf in config:
            if db_conf.valid & (query_type == "columnQuery"):
                cls.insert_column_names(db_conf, event)
            elif db_conf.valid & (query_type == "sqlQuery"):
                cls.general_query_event(db_conf, event)


def setup_query_listeners():
    subscribe("query_execution", QueryOperation.run_query)
