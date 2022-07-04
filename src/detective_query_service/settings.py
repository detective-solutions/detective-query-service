# import standard modules
import os
from typing import Optional

# import third party modules
import pydgraph
from dotenv import load_dotenv


load_dotenv()


def read_env(variable_name: str) -> Optional[str]:
    variable = os.getenv(variable_name)
    if (variable != "") & (variable is not None):
        return variable
    else:
        raise ValueError(f"Environment Variable {variable_name} is missing")


# set dgraph host
DGRAPH_HOST = read_env("DGRAPH_SERVICE_NAME")
DGRAPH_PORT = read_env("DGRAPH_PORT")
DGRAPH_SERVER = f"{DGRAPH_HOST}:{DGRAPH_PORT}"

# set kafka host
KAFKA_HOST = read_env("KAFKA_SERVICE_NAME")
KAFKA_PORT = read_env("KAFKA_PORT")
KAFKA_SERVER = f"{KAFKA_HOST}:{KAFKA_PORT}"

# set trino host
TRINO_HOST = read_env("TRINO_SERVICE_NAME")
TRINO_PORT = read_env("TRINO_PORT")
TRINO_SERVER = f"{TRINO_HOST}:{TRINO_PORT}"

# set dgraph connection
dgraph_client_stub = pydgraph.DgraphClientStub(DGRAPH_SERVER)
dgraph_client = pydgraph.DgraphClient(dgraph_client_stub)
