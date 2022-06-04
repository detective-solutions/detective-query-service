# import project related modules
from detective_query_service.service.producer import producer
from detective_query_service.service.event import subscribe, post_event
from detective_query_service.pydataobject.transformer import EventOperation
import json


class KafkaOperation:

    @classmethod
    def create_casefile_event(cls, data) -> None:
        event = EventOperation.create_casefile_event(data)
        producer.send("casefile", value=event.dict())

    @classmethod
    def create_masking_event(cls, data) -> None:
        event = EventOperation.read_masking_event({
            "context": data.get("context").dict(),
            "body": data.get("body").dict()
        })

        producer.send("masking", value=event.dict())
        print("send masking event with: ", json.dumps(event.dict(), indent=4), " After producer.send")


def setup_kafka_event_handlers():
    subscribe("kafka_casefile_response", KafkaOperation.create_casefile_event)
    subscribe("kafka_masking_response", KafkaOperation.create_masking_event)
