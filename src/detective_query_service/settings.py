# import third party modules
import pydgraph

# import project related modules
from detective_query_service.connectors.sql.sql_connector import SQLConnector
from detective_query_service.connectors.mongodb.mongodb_connector import MongoDBConnector


# set dgraph connection
dgraph_client_stub = pydgraph.DgraphClientStub('localhost:9080')
dgraph_client = pydgraph.DgraphClient(dgraph_client_stub)

# connector selection

connectors = {
    "mysql": SQLConnector,
    "postgresql": SQLConnector,
    "mariadb": SQLConnector,
    "mssql": SQLConnector,
    "orcale": SQLConnector,
    "mongodb": MongoDBConnector
}
