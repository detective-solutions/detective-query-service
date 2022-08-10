# import project related module
from detective_query_service.settings import dgraph_client
from detective_query_service.database.execution import execute_query


def get_source_by_table_xid(table_xid: list) -> dict:
    """
    Function to receive a database configuration in dgraph by providing a table_xid
    :param table_xid: list with table_xid from dgraph in uuid format
    :return: returns query results in json format
    """
    inner_params = ", ".join(f"$source{i}" for i in range(len(table_xid)))
    outer_params = ", ".join(f"$source{i}: string" for i in range(len(table_xid)))
    variables = {f"$source{i}": s for i, s in enumerate(table_xid)}
    query = f'''
        query tables({outer_params})''' + '''{result(func: eq(dgraph.type, "Table"))
        @filter(eq(Table.xid, [''' + f'''{inner_params}''' + '''])) {
                source: Table.dataSource {
                    name: SourceConnection.name
                    host: SourceConnection.host
                    port: SourceConnection.port
                    user: SourceConnection.user
                    password: SourceConnection.password
                    database: SourceConnection.database
                    databaseSchema: SourceConnection.databaseSchema
                    connectorName: SourceConnection.connectorName
                }
            }
        }
    '''

    res = execute_query(client=dgraph_client, query=query, variables=variables)
    if type(res) == dict:
        query_result = res
        query_result = {"result": [x.get("source") for x in query_result["result"]]}
    else:
        query_result = {"error": ["0001: query was not successful contact support"]}
    return query_result


def get_source_by_source_xid(source_xid: str) -> dict:
    """
    Function to receive a database configuration in dgraph by providing a table_xid
    :param source_xid: uid from dgraph
    :return: returns query results in json format
    """
    variables = {"$source_0": source_xid}
    query = '''
        query sources($source_0: string)''' + '''{
            result(func: uid($source_0)) {
                name: SourceConnection.name
                host: SourceConnection.host
                port: SourceConnection.port
                user: SourceConnection.user
                password: SourceConnection.password
                database: SourceConnection.database
                databaseSchema: SourceConnection.databaseSchema
                connectorName: SourceConnection.connectorName
            }
        }
    '''

    res = execute_query(client=dgraph_client, query=query, variables=variables)
    if type(res) == dict:
        query_result = res
        query_result = {"result": query_result["result"]}
    else:
        query_result = {"error": ["0001: query was not successful contact support"]}
    return query_result
