from detective_query_service.service.listeners.query_listener import setup_query_listeners
from detective_query_service.service.listeners.kafka_listener import setup_kafka_event_handlers


def initialize_listeners() -> None:
    setup_query_listeners()
    setup_kafka_event_handlers()
