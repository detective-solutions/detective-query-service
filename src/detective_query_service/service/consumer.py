# import standard modules
import json

# import third party modules
from kafka import KafkaConsumer

# import project related modules
from detective_query_service.settings import KAFKA_SERVER
from detective_query_service.utils.query import execute_query
from detective_query_service.service.operations import Operation
from detective_query_service.service.producer import query_producer
from detective_query_service.graphql.databases import get_source_by_table_uid


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

    for i, config in enumerate(db_configs["result"]):

        # TODO: find out how it works with no sql
        # TODO: check blob stores for files
        catalog = config.get("name", "")
        schema_db = config.get("schema", "")
        query = message.get("query")[0]
        requirement_list = [catalog, schema_db, query]

        if None in requirement_list:
            topic, value = Operation.missing_definition_event(requirement_list)

        else:
            schema, data = execute_query(catalog, schema_db, query)

            if event_type == "find_columns_first":
                topic, value = Operation.find_columns_first_event(data, schema, message, config, i)

            elif event_type == "general":
                topic, value = Operation.general_query_event(data, schema, message, config, i)

        query_producer.send(topic, value=value)
