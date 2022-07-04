# import standard modules
import json

# import third party modules
from kafka import KafkaProducer
from detective_query_service.settings import KAFKA_SERVER


producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    retries=5,
    key_serializer=lambda x: json.dumps(x).encode("utf-8"),
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    api_version=(0, 10, 2)
)
producer.flush()
