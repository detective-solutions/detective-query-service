# import standard modules
import os

# import third party modules
import pydgraph
from dotenv import load_dotenv


load_dotenv(".env")

# set dgraph host
DGRAPH_HOST = os.getenv("DGRAPH_SERVICE_NAME")
DGRAPH_PORT = os.getenv("DGRAPH_PORT")
assert (DGRAPH_HOST != "") & (DGRAPH_PORT != ""), "DGRAPH Variables not provided"
DGRAPH_SERVER = f"{DGRAPH_HOST}:{DGRAPH_PORT}"

# set kafka host
KAFKA_HOST = os.getenv("KAFKA_SERVICE_NAME")
KAFKA_PORT = os.getenv("KAFKA_PORT")
assert (KAFKA_HOST != "") & (KAFKA_PORT != ""), "KAFKA Variables not provided"
KAFKA_SERVER = f"{KAFKA_HOST}:{KAFKA_PORT}"

# set trino host
TRINO_HOST = os.getenv("TRINO_SERVICE_NAME")
TRINO_PORT = os.getenv("TRINO_PORT")
assert (TRINO_HOST != "") & (TRINO_PORT != ""), "TRINO Variables not provided"
TRINO_SERVER = f"{TRINO_HOST}:{TRINO_PORT}"

# set dgraph connection
dgraph_client_stub = pydgraph.DgraphClientStub(DGRAPH_SERVER)
dgraph_client = pydgraph.DgraphClient(dgraph_client_stub)