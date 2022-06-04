# standard modules
import logging

# import project related modules
from detective_query_service.service.event import subscribe
from detective_query_service.pydataobject.event_type import Context, QueryEvent

logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


def construct_context_log(context: Context) -> str:
    prefix = f"{context.tenantId}:{context.casefileId}:{context.nodeId}:{context.eventType}:{context.userId}:"
    return prefix


def kafka_response_error(context: Context) -> None:
    logging.error(f"{construct_context_log(context)} kafka response could not be created")


def kafka_masking_response(data: dict) -> None:
    context = data.get("context", None)
    if context is not None:
        logging.info(f"{construct_context_log(context)} find_columns_first_event for {context.casefileId} executed")


def missing_follow_event(data: QueryEvent) -> None:
    context = data.context
    logging.error(f"{construct_context_log(context)} no follow event was provided for insert column names to query")


def insert_column_name_error(context: Context) -> None:
    logging.error(f"{construct_context_log(context)} insert_column_names cloud not be executed")


def invalid_query_event(data: None) -> None:
    logging.error("QueryEvent received event of type 'None' or Config of type 'None'")


def invalid_query_key(data: None) -> None:
    logging.error("QueryEvent received event does miss either event or config")


def query_execution(data: dict) -> None:
    context = data.get("event", None)
    if context is not None:
        logging.info(f"{construct_context_log(context.context)} received query event and start execution")


def invalid_message(data: None) -> None:
    logging.error("Invalid message received by kafka")


def setup_log_event_handlers():
    subscribe("kafka_response_error", kafka_response_error)
    subscribe("kafka_masking_response", kafka_masking_response)
    subscribe("missing_follow_event", missing_follow_event)
    subscribe("insert_column_name_error", insert_column_name_error)
    subscribe("invalid_query_event", invalid_query_event)
    subscribe("invalid_query_key", invalid_query_key)
    subscribe("query_execution", query_execution)
    subscribe("invalid_message", invalid_message)
