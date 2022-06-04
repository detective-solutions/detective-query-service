# import third party modules
import pandas as pd


def get_column_definitions(data_object: pd.DataFrame) -> list:
    column_defs = [
        {'headerName': column, 'field': column, 'sortable': True, 'filter': True}
        for column in data_object.columns.tolist()
    ]
    return column_defs
