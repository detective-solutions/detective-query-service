# import standard modules
import json
from typing import Tuple, Any
from dataclasses import asdict
from operator import itemgetter

# import third party modules
import pandas as pd

# import project related modules
from detective_query_service.log_definition import logger
from detective_query_service.events.event_type import QueryEvent
from detective_query_service.utils.query import transform_generic_to_specific_selection_query


class Operation:

    @classmethod
    def missing_definition_event(cls, requirement_list: list) -> Tuple[str, Any]:
        index_title = ["name", "database schema", "query"]
        indexes = [ix for ix in requirement_list if ix is None]
        data = pd.DataFrame({"error": list(itemgetter(*indexes)(index_title))})
        schema = {'headerName': "error", 'field': "error", 'sortable': True, 'filter': True}

        result = {
            "query": "",
            "schema": schema,
            "data": json.loads(data.to_json(orient="records"))
        }

        return "casefiles", result

    @classmethod
    def find_columns_first_event(cls, data: pd.DataFrame, schema: dict, message: dict,
                                 config: dict, enumerator: int) -> Tuple[str, Any]:

        columns_from_tables = list()
        follow_event = message.get("follow_query_event")

        if "error" not in data.columns.tolist():
            columns_from_tables.extend(data.Column.tolist())

            event = QueryEvent(
                case=follow_event.get("case", ""),
                event_type="general",
                source=follow_event.get("source", list()),
                query=[
                    transform_generic_to_specific_selection_query(
                        follow_event.get("query")[0],
                        columns_from_tables
                    )
                ],
                groups=follow_event.get("groups", list()),
                follow_query_event=dict()
            )
            logger.info(f"find_columns_first_event for {follow_event.get('case', '')} executed")
            return "masking", asdict(event)

        else:
            logger.info(f"query was not successful {follow_event.get('case', '')}")
            return "casefile", json.loads(data.to_json(orient="records"))

    @classmethod
    def general_query_event(cls, data: pd.DataFrame, schema: dict, message: dict,
                            config: dict, enumerator: int) -> Tuple[str, Any]:
        result = {
            "query": message.get("query")[enumerator],
            "schema": schema,
            "data": json.loads(data.to_json(orient="records"))
        }

        logger.info(f"general_query_event for {message.get('case', '')} executed")
        return "casefile", result

        # elif event_type == "source_crawl":
        #    if message.get("source", dict()).get("xid") == "69fd6ba6-aec2-4acc-a8c7-a74974d55b63":
        #        config = message.get("source")
        #        tenant = message.get("tenant")

        #        conn = connect(
        #             host="localhost",
        #            port="8080",
        #            user="root",
        #            catalog="elephant",
        #            schema="public"
        #        )

        #        snapshot = conn.crawl_database(config.get("xid"))

        #        data = SourceSnapshot(
        #            tenant=tenant,
        #                source=config.get("xid"),
        #            snapshot=snapshot
        #        )
        #        print("send: ", asdict(data))
        #        query_producer.send("version-control", value=asdict(data))
        #        logger.info(f"send crawl event results for source {config.get('xid', '')}")