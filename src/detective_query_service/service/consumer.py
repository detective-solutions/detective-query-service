# import standard modules
import json

# import third party modules
from kafka import KafkaConsumer

# import project related modules
from detective_query_service.settings import KAFKA_SERVER
from detective_query_service.utils.query import execute_query
from detective_query_service.pydataobject.event_type import QueryEvent
from detective_query_service.pydataobject.transformer import EventOperation
from detective_query_service.database.databases import get_source_by_table_xid
from detective_query_service.service.event import post_event
from detective_query_service.service.listeners.registration import initialize_listeners


consumer = KafkaConsumer(
    "query_execution",
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="query-service",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    api_version=(0, 10, 2)
)

initialize_listeners()
for message in consumer:

    message = message.value
    event = EventOperation.read_query_event(message)
    db_configs = get_source_by_table_xid(table_xid=event.body.tableId)
    db_configs = EventOperation.read_database_config(event.context, db_configs.get("result", {}))
    post_event("query_execution", {"event": event, "config": db_configs})
    import time
    time.sleep(10)