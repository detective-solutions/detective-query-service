# import third party modules
import pydgraph

# Variables
DGRAPH_HOST = 'localhost:9080'
KAFKA_HOST = 'localhost:9093'

# set dgraph connection
dgraph_client_stub = pydgraph.DgraphClientStub(DGRAPH_HOST)
dgraph_client = pydgraph.DgraphClient(dgraph_client_stub)
