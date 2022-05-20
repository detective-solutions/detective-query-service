# import third party modules
import pandas as pd

# import project related modules
from detective_query_service.log_definition import logger


def get_column_definitions(data_object: pd.DataFrame) -> list:

    logger.info(f"column_definition incoming: type: {type(data_object)} - {data_object}")
    column_defs = [
        {'headerName': column, 'field': column, 'sortable': True, 'filter': True}
        for column in data_object.columns.tolist()
    ]
    return column_defs
