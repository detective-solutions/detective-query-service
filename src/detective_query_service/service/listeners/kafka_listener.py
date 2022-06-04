# import project related modules
from detective_query_service.service.producer import producer
from detective_query_service.service.event import subscribe, post_event
from detective_query_service.pydataobject.transformer import EventOperation


class KafkaOperation:

    @classmethod
    def create_casefile_event(cls, data: dict) -> None:
        """
        creates and sends a kafka event to the casefile topic which holds a data frame to be visualised
        on the client side
        :param data: key value map holding {"body": type CaseFileBody as dict, "context": type Context as dict}
        """
        try:
            event = EventOperation.create_casefile_event(data)
            producer.send("casefile", value=event.dict())
        except Exception:
            post_event("kafka_response_error", data)

    @classmethod
    def create_masking_event(cls, data) -> None:
        """
        creates and sends a kafka event to the masking topic
        :param data: key value map holding {"body": type QueryBody, "context": type Context}
        """
        try:
            event = EventOperation.read_masking_event({
                "context": data.get("context").dict(),
                "body": data.get("body").dict()
            })
            producer.send("masking", value=event.dict())

        except Exception:
            post_event("kafka_response_error", data)


def setup_kafka_event_handlers():
    subscribe("kafka_casefile_response", KafkaOperation.create_casefile_event)
    subscribe("kafka_masking_response", KafkaOperation.create_masking_event)
