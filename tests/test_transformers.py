# import third party modules
import pytest

# import project related modules
from detective_query_service.transformers.response import get_valid_column_names, get_column_definitions


@pytest.mark.parametrize("test_set", [
    (["Banana_split"], ["Banana_split"]),
    (["Banana(split"], ["Banana_split"]),
    (["82 Banana*split"], ["Banana_split"])
])
def test_get_valid_column_names(test_set):
    test_values, expected_result = test_set
    result = get_valid_column_names(test_values)
    assert result == expected_result, f"{result} does not match {expected_result}"


@pytest.mark.parametrize("data", [
    {"test_column": [1, 2, 3, 4]},
    {"test(column)": ["a", "b", "c"]}
])
def test_get_column_definitions(data):
    expected = [{'headerName': "test_column", 'field': "test_column", 'sortable': True, 'filter': True}]
    column_defs = get_column_definitions(data)
    assert column_defs == expected, f"{column_defs} does not match {expected}"
