# import standard modules
import json
from dataclasses import asdict

# import third party modules
from kafka import KafkaConsumer

# import project related modules
from detective_query_service.settings import KAFKA_SERVER
from detective_query_service.log_definition import logger
from detective_query_service.service.producer import query_producer
from detective_query_service.connectors.general.factory import connector
from detective_query_service.graphql.databases import get_source_by_table_uid
from detective_query_service.events.event_type import QueryEvent, SourceSnapshot
from detective_query_service.transformers.query import transform_generic_to_specific_selection_query


query_consumer = KafkaConsumer(
    "query_execution",
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="query-service",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    api_version=(0, 10, 2)
)

for message in query_consumer:

    message = message.value

    db_configs = get_source_by_table_uid(table_xid=message.get("source"))
    event_type = message.get("event_type")

    if event_type == "find_columns_first":
        columns_from_tables = list()
        for i, config in enumerate(db_configs["result"]):

            conn = connector(**config)
            schema, data = conn.execute_query(message.get("query")[i])
            columns_from_tables.extend(data.get("column_name"))

        follow_event = message.get("follow_query_event")
        data = QueryEvent(
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
        query_producer.send("masking", value=asdict(data))
        logger.info(f"send general query event for case {follow_event.get('case', '')}")

    elif event_type == "general":
        print("general", message)
        for i, config in enumerate(db_configs["result"]):

            conn = connector(**config)
            schema, data = conn.execute_query(message.get("query")[i])

            result = {"query": message.get("query")[i], "schema": schema, "data": data}
            query_producer.send("casefile", value=result)

    elif event_type == "source_crawl":
        if message.get("source", dict()).get("xid") == "69fd6ba6-aec2-4acc-a8c7-a74974d55b63":
            config = message.get("source")
            tenant = message.get("tenant")
            conn = connector(**config)
            snapshot = conn.crawl_database(config.get("xid"))

            data = SourceSnapshot(
                tenant=tenant,
                source=config.get("xid"),
                snapshot=snapshot
            )
            print("send: ", asdict(data))
            query_producer.send("version-control", value=asdict(data))
            logger.info(f"send crawl event results for source {config.get('xid', '')}")







