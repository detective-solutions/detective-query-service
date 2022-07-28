# import standard modules
import json

# import third party modules
from kafka import KafkaConsumer

# import project related modules
from detective_query_service.settings import KAFKA_SERVER
from detective_query_service.service.event import post_event
from detective_query_service.pydataobject.transformer import EventOperation
from detective_query_service.service.listeners.registration import initialize_listeners
from detective_query_service.database.databases import get_source_by_table_xid, get_source_by_source_xid


consumer = KafkaConsumer(
    "query_execution",
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    api_version=(0, 10, 2)
)

initialize_listeners()

for message in consumer:

    try:
        message = message.value
        eventType = message.get("context", {}).get("eventType", None)
        if (eventType is not None) & (eventType == "crawlQuery"):
            crawl_event = EventOperation.read_crawl_event(message)
            config = get_source_by_source_xid(crawl_event.body.sourceId)
            post_event("source_crawl", config)
        else:
            query_event = EventOperation.read_query_event(message)
            config_list = get_source_by_table_xid(table_xid=query_event.body.tableId)
            db_configs = EventOperation.read_database_config(query_event.context, config_list.get("result", {}))
            post_event("query_execution", {"event": query_event, "config": db_configs})

    except Exception:
        post_event("invalid_message", None)
        continue
