# import standard modules
import json
from typing import List

# import project related modules
from detective_query_service.service.event import subscribe, post_event
from detective_query_service.pydataobject.dgraph_type import DataBaseConfig
from detective_query_service.pydataobject.event_type import QueryEvent, Context
from detective_query_service.utils.query import transform_generic_to_specific_selection_query, execute_query, get_source_snapshot


class QueryOperation:

    @classmethod
    def insert_column_names(cls, config: DataBaseConfig, event: QueryEvent) -> None:
        """
        function to replace the wildcard character in a sql statement and replaces it with explict column names.
        It will update the provided QueryEvent and creates a new one with the assigned follow event
        :param config: database configuration used to query against trino
        :param event: QueryEvent to be modified
        """
        try:
            schema, data = execute_query(config, event)
            follow_event = event.body.followEvent

            if "error" not in data.columns.tolist():
                if follow_event is not None:
                    follow_event.query = [
                        transform_generic_to_specific_selection_query(
                            follow_event.query[0],
                            data.Column.tolist()
                        )
                    ]
                    post_event("kafka_masking_response", {"body": follow_event, "context": event.context})
                else:
                    post_event("missing_follow_event", event)

            else:
                cls.construct_casefile_response(
                    query_type=event.body.queryType,
                    query=event.body.query,
                    schema=schema,
                    data=json.loads(data.to_json(orient="records")),
                    context=event.context
                )

        except Exception:
            post_event("insert_column_name_error", event.context)

    @classmethod
    def general_query_event(cls, config: DataBaseConfig, event: QueryEvent) -> None:
        """
        function to execute a QueryEvent against Trino
        :param config: database configuration used to query against trino
        :param event: QueryEvent to be executed
        """
        schema, data = execute_query(config, event)
        cls.construct_casefile_response(
            query_type=event.body.queryType,
            query=event.body.query,
            schema=schema,
            data=json.loads(data.to_json(orient="records")),
            context=event.context
        )

    @classmethod
    def construct_casefile_response(cls, query_type: str, query: List[str], schema: List[dict],
                                    data: List[dict], context: Context) -> None:
        """
        function to construct and launch a general casefile response for a table with provided values
        :param query_type: type of query which will be executed
        :param query: list of queries to be executed
        :param schema: schema of the response table
        :param data: data of the response table
        :param context: context the response belongs to
        """

        result = {
            "queryType": query_type,
            "query": query,
            "tableSchema": schema,
            "tableData": data
        }

        post_event("kafka_casefile_response", {"body": result, "context": context})

    @classmethod
    def run_query(cls, request: dict) -> None:
        """
        manager method which will trigger the right processing for a given query event based on the query type
        :param request: key value pair of the QueryEvent and the database configuration to be used for the query
        """
        try:
            event = request.get("event", None)
            config = request.get("config", None)

            try:
                query_type = event.body.queryType

                for db_conf in config:
                    if db_conf.valid & (query_type == "columnQuery"):
                        cls.insert_column_names(db_conf, event)
                    elif db_conf.valid & (query_type == "sqlQuery"):
                        cls.general_query_event(db_conf, event)

            except AttributeError:
                post_event("invalid_query_event", None)

        except KeyError:
            post_event("invalid_query_key", None)

    @classmethod
    def run_crawl(cls, request: dict) -> None:
        try:
            for config in request.get("result", list()):
                db_config = DataBaseConfig(**config)
                snapshot = get_source_snapshot(db_config)
                post_event("kafka_version_pub", {"snapType": "initialization", "snapshot": snapshot})
        except Exception as error:
            print("run crawl", error)


def setup_query_listeners():
    subscribe("query_execution", QueryOperation.run_query)
    subscribe("source_crawl", QueryOperation.run_crawl)
