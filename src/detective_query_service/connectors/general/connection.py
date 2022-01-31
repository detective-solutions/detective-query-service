# import standard modules
from typing import Any, Dict, Optional


class UninitializedAttributeError(Exception):
    pass


class Connector(object):

    def __init__(self, host: str, user: str, password: str, database: str, port: int, cluster: str = None,
                 api_token: str = None, **kwargs):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.api_token: Any = api_token
        self.cluster: Any = cluster
        self.__error_status = "None"
        self.__connection: Any
        self.connection_established = self._create_connection()

    def check_if_database_exist(self):
        return NotImplementedError

    def _query_restriction(self, query: str) -> bool:
        return False

    def get_databases(self):
        return NotImplementedError

    def get_tables(self):
        return NotImplementedError

    def _create_connection(self) -> bool:
        return False

    def execute_query(self, query: Any):
        return NotImplementedError

    @property
    def connection(self):
        return self.__connection

    @connection.setter
    def connection(self, value) -> None:
        self.__connection = value

    def _ensure_connection(self):
        if self.__connection is None:
            raise UninitializedAttributeError("connection is not initialized")
