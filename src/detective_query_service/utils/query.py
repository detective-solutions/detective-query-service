# import standard modules
import uuid

# import third party modules
import pandas as pd
from trino.dbapi import connect

# import project related modules
from detective_query_service.settings import TRINO_HOST, TRINO_PORT
from detective_query_service.pydataobject.event_type import QueryEvent
from detective_query_service.utils.response import get_column_definitions
from detective_query_service.pydataobject.dgraph_type import DataBaseConfig


def transform_generic_to_specific_selection_query(query: str, columns: list) -> str:
    """
    functions replaces wildcard character from string query with specific column names
    :param query: query to be modified
    :param columns: columns to be added
    :return: modified query
    """
    tokens = query.split(" ")
    columns_str = ", ".join(c for c in columns)
    new_query = "SELECT " + f"{columns_str} " + " ".join(t for t in tokens[2:])
    return new_query


def execute_query(config: DataBaseConfig, message: QueryEvent) -> tuple:
    """
    function runs a query event against trino with a given database configuration
    :param config: Configuration to be used for the connection
    :param message: QueryEvent to be executed
    :return: (schema as dict type, data as dict type)
    """

    try:
        conn = connect(
            host=TRINO_HOST,
            port=TRINO_PORT,
            user="root",
            catalog=config.name,
            schema=config.databaseSchema
        )

        data = pd.read_sql(message.body.query[0], conn)
        schema = get_column_definitions(data)

    except Exception as e:
        data = pd.DataFrame({"error": [str(e)]})
        schema = [{'headerName': "error", 'field': "error", 'sortable': True, 'filter': True}]

    return schema, data


def get_table_set(conn: connect) -> dict:
    tables = pd.read_sql("show tables", conn).Table.tolist()
    schema = dict()

    for table in tables:
        columns = pd.read_sql(f"describe {table}", conn).to_dict("records")
        schema[table] = [{
            "xid": str(uuid.uuid1()),
            "columnName": x.get("Column", ""),
            "columnType": x.get("Type", "")
        } for x in columns]

    return schema


def get_source_snapshot(config: DataBaseConfig) -> dict:
    try:
        conn = connect(
            host=TRINO_HOST,
            port=TRINO_PORT,
            user="root",
            catalog=config.name,
            schema=config.databaseSchema
        )
        snapshot = get_table_set(conn)
        return snapshot
    except Exception as error:
        print("get_source_snapshot", error)
        return {}
