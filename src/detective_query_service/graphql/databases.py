# import project related module
from detective_query_service.settings import dgraph_client
from detective_query_service.graphql.execution import execute_query


def get_source_by_table_uid(table_xid: list) -> dict:
    inner_params = ", ".join(f"$source{i}" for i in range(len(table_xid)))
    outer_params = ", ".join(f"$source{i}: string" for i in range(len(table_xid)))
    variables = {f"$source{i}": s for i, s in enumerate(table_xid)}
    query = f'''
        query tables({outer_params})''' + '''{result(func: eq(dgraph.type, "TableObject"))
        @filter(eq(TableObject.xid, [''' + f'''{inner_params}''' + '''])) {
                source: TableObject.dataSource {
                    host: SourceConnection.host
                    port: SourceConnection.port
                    password: SourceConnection.password
                    database: SourceConnection.database
                    user: SourceConnection.user
                    db_type: SourceConnection.db_type
                }
            }
        }
    '''

    res = execute_query(client=dgraph_client, query=query, variables=variables)
    if type(res) == dict:
        query_result = res

        # TODO: Check if it works with version control - since ("source")[0] does not work with query request
        query_result = {"result": [x.get("source") for x in query_result["result"]]}
    else:
        query_result = {"error": ["query was not successful"]}
    return query_result
