# import standard modules
import json

# import third party modules
from pydgraph import DgraphClient, AbortedError


def execute_query(client: DgraphClient, query: str, variables: dict) -> dict:
    """
    dgraph query execution function which will take a query and variables to post it against the dgraph server

    :param client: dgraph client
    :param query: string object in Dgraph Query Language (DQL) format
    :param variables: key value array holding variables used in the query
    :return: query result in json format
    """
    txn = client.txn()
    try:
        res = txn.query(query, variables=variables)
        res = json.loads(res.json)
        if type(res) == dict:
            query_result = res
        else:
            query_result = {"error": ["0002: query was not successful contact support"]}
        txn.discard()
        return query_result

    except AbortedError:
        query_result = {"error": ["0003 query was not successful contact support"]}
        txn.discard()
        return query_result
