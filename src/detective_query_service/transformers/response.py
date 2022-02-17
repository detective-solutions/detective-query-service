

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


def get_column_definitions(data_object: dict) -> list:
    columns = get_valid_column_names(list(data_object.keys()))
    column_defs = [
        {'headerName': column, 'field': column, 'sortable': True, 'filter': True}
        for column in columns
    ]
    return column_defs
