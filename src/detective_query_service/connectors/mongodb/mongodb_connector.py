# import standard modules
import urllib.parse
from typing import Dict, List, Any

# import third party modules
from pymongo import MongoClient

# import project related modules
from detective_query_service.logging import logger
from detective_query_service.connectors.general.connection import Connector


class MongoDBConnector(Connector):
    """
    This Connector is a wrapper around the pymongo Module from python wich provides access to MongoDBs.
    One can easily use the class to connect to any of these databases by providing the following parameters:

     :param host: host e.g: 6funv.mongodb.net
     :param user: username
     :param password: password related to user and database
     :param database: databse name
     :param port: port number as integer
     :param cluster: clustername e.g. cluster0 as string
    """

    def __init__(self, host: str, user: str, password: str, database: str, port: int = 27017, cluster="cluster0",
                 **kwargs):
        super().__init__(host, user, password, database, port, cluster)
        self.connected_database: Any

    def _get_connection_string(self) -> str:
        """
        function to create the string of connection used by the engine.

        :return: returns a connection address as string
        """

        password = urllib.parse.quote(self.password.encode('utf8'))
        return f'mongodb+srv://{self.user}:{password}@{self.cluster}.{self.host}/{self.database}'

    def _create_connection(self) -> bool:
        """
        creates the engine and connection to a given database configuration

        :return: Ture if creating a connection was successful, False otherwise
        """
        try:
            self.connection = MongoClient(self._get_connection_string(), readPreference='secondary')
            self.connected_database = self.connection[self.database]
            return True

        except Exception as connection_exception:
            logger.error(str(connection_exception))
            return False

    def _query_restriction(self, query: str) -> bool:
        pass

    def close(self):
        self.connection.close()

    def execute_query(self, query: dict) -> Dict[str, List]:
        """
        executes a given query of selection operation for the created databse connection

        :param query: query dict in pymongo syntax
        :param table: table name which the query goes to
        :return: a dict with key and list object
        """
        try:
            if self.connected_database is not None:
                table = query.get("table_name", "")
                collection = self.connected_database[table]
                results = list()

                for line in collection.find(query.get("query")):
                    results.append(line)

                return {k: [d.get(k, None) for d in results] for k in results[0]}
            else:
                return {"error": [f"database connection does not exist for {table}"]}

        except Exception as db_exception:
            logger.error(str(db_exception))
            return {"error": [str(db_exception)]}
