# import third party modules
import pydgraph


# set dgraph connection
dgraph_client_stub = pydgraph.DgraphClientStub('localhost:9080')
dgraph_client = pydgraph.DgraphClient(dgraph_client_stub)
