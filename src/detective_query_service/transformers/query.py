
def transform_generic_to_specific_selection_query(query: str, columns: list) -> str:
    tokens = query.split(" ")
    columns_str = ", ".join(c for c in columns)
    new_query = "SELECT " + f"{columns_str} " + " ".join(t for t in tokens[2:])
    return new_query
