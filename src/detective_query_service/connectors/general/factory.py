# import project related modules
from detective_query_service.connectors.sql.sql_connector import SQLConnector
from detective_query_service.connectors.mongodb.mongodb_connector import MongoDBConnector


class Connector:

    def __init__(self, db_type: str):
        self.db_type = db_type
        self.connector = self.get_type()

    def get_type(self):
        if self.db_type in ["mysql", "postgresql", "mariadb", "mssql", "oracle"]:
            return SQLConnector
        elif self.db_type == "mongodb":
            return MongoDBConnector
        else:
            return SQLConnector

    def execute_query(self, query: str):
        return self.connector.execute_query(query)
