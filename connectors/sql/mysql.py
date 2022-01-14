# import standard modules

# import third party modules
import mysql.connector
from mysql.connector.errors import *

# import project related modules
from ..general.connection import Connector


class MySQLConnector(Connector):

    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        super().__init__(host, user, password, database, port)

    def create_connection(self) -> None:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

        except DatabaseError as db_exception:
            self.error_status = str(db_exception)

    def execute_query(self, query: str) -> list:
        try:
            if self.query_restriction(query):
                return [("error", "query tries to create, alter, show or use sys information")]

            else:
                cursor = self.connection.cursor()
                cursor.execute(f'''{query}''')
                result = cursor.fetchall()
                return result

        except Exception as db_exception:
            print(db_exception)

    def query_restriction(self, query: str) -> bool:
        keywords = ["create", "alter", "show", "sys"]
        query = query.replace(".", " ").split(" ")
        to_restrict = 4 > len(set(keywords) - set(query))
        return to_restrict

