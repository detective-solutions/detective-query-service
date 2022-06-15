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


#consumer = KafkaConsumer(
#    "query_execution",
#    bootstrap_servers=[KAFKA_SERVER],
#    auto_offset_reset="earliest",
#    enable_auto_commit=True,
#    group_id="query-service",
#    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
#    api_version=(0, 10, 2)
#)

initialize_listeners()

consumer_l = [
    {
       "context": {
          "tenantId": "c50416fc-ec70-11ec-858d-9cb6d0fe269b",
          "timestamp": "2022-01-01T12:01:00",
          "eventType": "crawlQuery",
          "userId": "root",
          "valid": True,
          # "userRole": None
       },
       "body": {
          "sourceId": "0x1"
       }
    }
]

for message in consumer_l:

    try:
        # message = message.value
        eventType = message.get("context", {}).get("eventType", None)
        if (eventType is not None) & (eventType == "crawlQuery"):
            event = EventOperation.read_crawl_event(message)
            config = get_source_by_source_xid(event.body.sourceId)
            post_event("source_crawl", config)
        else:
            event = EventOperation.read_query_event(message)
            config_list = get_source_by_table_xid(table_xid=event.body.tableId)
            db_configs = EventOperation.read_database_config(event.context, config_list.get("result", {}))
            post_event("query_execution", {"event": event, "config": db_configs})

    except Exception as error:
        # print("error: ", error)
        post_event("invalid_message", None)
