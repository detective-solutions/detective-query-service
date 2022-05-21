# import standard modules
import json

# import third party modules
import pytest

# import project related modules
from detective_query_service.utils.tuples import tuple_to_json
from detective_query_service.utils.response import get_column_definitions


def test_get_column_definitions(dummy_data):
    expected = [{'headerName': "test_column", 'field': "test_column", 'sortable': True, 'filter': True}]
    column_defs = get_column_definitions(dummy_data)
    assert column_defs == expected, f"{column_defs} does not match {expected}"


def test_tuple_to_json(dummy_data):
    keys = ["test_column"]
    tup = [(0,), (1,), (2,), (3,), (4,)]
    expected = json.loads(dummy_data.to_json(orient="records"))
    result = tuple_to_json(keys, tup)
    assert result == expected, f"{result} does not match {expected}"
