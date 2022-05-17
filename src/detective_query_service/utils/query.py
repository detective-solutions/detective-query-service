# import third party modules
import pandas as pd
from trino.dbapi import connect

# import project related modules
from detective_query_service.utils.response import get_column_definitions


def transform_generic_to_specific_selection_query(query: str, columns: list) -> str:
    tokens = query.split(" ")
    columns_str = ", ".join(c for c in columns)
    new_query = "SELECT " + f"{columns_str} " + " ".join(t for t in tokens[2:])
    return new_query


def execute_query(catalog: str, schema: str, query: str) -> tuple:
    conn = connect(
        host="localhost",
        port="8080",
        user="root",
        catalog=catalog,
        schema=schema
    )

    data = pd.read_sql(query, conn)
    schema = get_column_definitions(data)
    return schema, data
