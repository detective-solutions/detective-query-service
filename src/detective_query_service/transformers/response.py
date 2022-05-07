from detective_query_service.log_definition import logger


def get_valid_column_names(column_names: list) -> list:
    new_names = list()
    for column in column_names:
        column = column.lstrip('0123456789.- ')
        special_symbols = r"[ \ ( \ [ ] . * ? [ \ ) \ ] ]".split(" ")
        column = ''.join(x if x not in special_symbols
                         else "_" for x in column.split(" "))
        for sym in special_symbols:
            column = column.replace(sym, "_")
        column = column[:-1] if column.endswith("_") else column
        new_names.append(column)

    return new_names


def get_column_definitions(data_object: list) -> list:
    logger.info(f"column_definition incoming: type: {type(data_object)} - {data_object}")
    columns = get_valid_column_names(list(data_object[0].keys()))
    column_defs = [
        {'headerName': column, 'field': column, 'sortable': True, 'filter': True}
        for column in columns
    ]
    return column_defs
