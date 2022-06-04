from detective_query_service.service.listeners.query_listener import setup_query_listeners
from detective_query_service.service.listeners.log_listener import setup_log_event_handlers
from detective_query_service.service.listeners.kafka_listener import setup_kafka_event_handlers


def initialize_listeners() -> None:
    setup_query_listeners()
    setup_kafka_event_handlers()
    setup_log_event_handlers()
