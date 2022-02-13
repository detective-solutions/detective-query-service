# import standard modules
import urllib

# import third party modules
from pymongo import MongoClient

# import project related modules
# from src.detective_query_service.connectors.mongodb.mongodb_connector import MongoDBConnector


def test_create_mongo_dummy_data(nosql_database_configs, nosql_database_setup_queries):
    config = nosql_database_configs.get("mongodb", None)
    setup_queries = nosql_database_setup_queries.get("mongodb", None)

    if (config is not None) and (setup_queries is not None):
        user = config.get("user", "")
        password = config.get("password", "")
        host = config.get("host", "")
        port = config.get("port", 3306)
        database = config.get("database", "")

        password = urllib.parse.quote(password.encode('utf8'))
        cluster_url = f"{host}:{port}"
        connection_string = f'mongodb+srv://{user}:{password}@{cluster_url}/{database}'
        client = MongoClient(connection_string)
        assert client.closed is not True, "mongo db connection might not be established"


def test_create_mongo_connection(nosql_database_connections):
    pass


def test_execute_mongo_query_with_restricted_values(nosql_database_connections):
    pass


def test_execute_mongo_query_with_legitimate_values(nosql_database_connections, nosql_database_setup_queries):
    pass


def test_retrieve_mongo_tables_in_database(sql_database_connections, sql_database_setup_queries):
    pass
