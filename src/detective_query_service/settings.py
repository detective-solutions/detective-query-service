# import standard modules
import logging

# import third party modules
import pydgraph

# Set logging source
logging.basicConfig()
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('testfile.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# set dgraph connection
dgraph_client_stub = pydgraph.DgraphClientStub('localhost:9080')
dgraph_client = pydgraph.DgraphClient(dgraph_client_stub)
