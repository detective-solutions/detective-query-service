# import project related modules
from detective_query_service.connectors.sql.sql_connector import SQLConnector
from detective_query_service.connectors.mongodb.mongodb_connector import MongoDBConnector


def connector(db_type: str):
    if db_type in ["mysql", "postgresql", "mariadb", "mssql", "oracle"]:
        return SQLConnector
    elif db_type == "mongodb":
        return MongoDBConnector
    else:
        return SQLConnector
