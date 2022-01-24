# import third party module
from pydgraph import DgraphClient

# import project related module
from detective_query_service.graphql.execution import execute_query


def get_database_by_xid(client: DgraphClient, xid: str) -> dict:

    query = '''
        query sourceConnection($number: string) {
              result (func: eq(dgraph.type, "SourceConnection")) @filter(eq(xid, $number)) {
                xid
                host
                password
                database
                user
                db_type
              }
        }
    '''
    variables = {"$number": xid}
    res = execute_query(client, query, variables)

    if type(res) == dict:
        query_result = res
    else:
        query_result = {"error": ["query was not successful"]}

    return query_result
