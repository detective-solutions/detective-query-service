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


# query_consumer = KafkaConsumer(
#     "query_execution",
#     bootstrap_servers=[KAFKA_SERVER],
#     auto_offset_reset="earliest",
#     enable_auto_commit=True,
#     group_id="query-service",
#     value_deserializer=lambda x: json.loads(x.decode("utf-8")),
#     api_version=(0, 10, 2)
# )

import uuid
consumer = [
    {
        "context": {
            "tenantId": str(uuid.uuid1()),
            "casefileId": str(uuid.uuid1()),
            "timestamp": "2022-05-21 19:12:48.668",
            "eventType": "sqlQuery",
            "userId": str(uuid.uuid1()),
            "userRole": "normal",
            "nodeId": str(uuid.uuid1())
        },
        "body": {
            'queryType': 'sqlQuery', # 'columnQuery',
            'query': ['select id, query_type from myTable'], # ['SHOW COLUMNS FROM freequery'],
            'tableId': ['59c9547a-dea7-11ec-ac54-287fcf6e439d'],
            'executedQuery': None,
            'followEvent': {
                'queryType': 'sqlQuery',
                'query': ['SELECT * FROM freequery LIMIT 100'],
                'tableId': ['59c9547a-dea7-11ec-ac54-287fcf6e439d'],
                'executedQuery': None,
                'followEvent': None
            }
        }
    }
]

initialize_listeners()
for message in consumer:

    # message = message.value
    event = EventOperation.read_query_event(message)
    db_configs = get_source_by_table_xid(table_xid=event.body.tableId)
    db_configs = EventOperation.read_database_config(event.context, db_configs.get("result", {}))
    print("query_execution", {"event": event, "config": db_configs})
    post_event("query_execution", {"event": event, "config": db_configs})

        # TODO: find out how it works with no sql
        # TODO: check blob stores for files
    #    catalog = config.get("name", "")
    #    schema_db = config.get("schema", "")sd
    #    query = message.get("query")[0]
    #    requirement_list = [catalog, schema_db, query]

     #   if None in requirement_list:
     #       topic, value = Operation.missing_definition_event(requirement_list)

      #  else:
      #      schema, data = execute_query(catalog, schema_db, query)

      #      if event_type == "find_columns_first":
      #          topic, value = Operation.find_columns_first_event(data, schema, message, config, i)

      #      elif event_type == "general":
      #          topic, value = Operation.general_query_event(data, schema, message, config, i)

      #  query_producer.send(topic, value=value)
