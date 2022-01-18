# import standard modules
from typing import List, Any, Tuple
# import third party modules
from sqlalchemy import text
from sqlalchemy import create_engine

# import project related modules
from ..general.connection import Connector


class MySQLConnector(Connector):

    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        super().__init__(host, user, password, database, port)

    def create_connection(self) -> bool:
        try:
            engine = create_engine(
                f"mysql://{self.user}:{self.password}@{self.host}/{self.database}",
                echo=True
            )
            self.connection = engine.connect()
            return True

        except Exception as db_exception:
            self.__error_status = str(db_exception)
            print(self.__error_status)
            return False

    def execute_query(self, query: str) -> List[Tuple[str, Any]]:
        try:
            if self.query_restriction(query):
                return [("error", "query tries to create, alter, show or use sys information")]

            else:

                self.ensure_connection()
                t = text(f'''{query}''')
                result = self.connection.execute(t).fetchall()
                if type(result) == list:
                    return result
                else:
                    return [("error", "fetched result is not a list of tuples")]

        except Exception as db_exception:
            return [("error", str(db_exception))]

    def query_restriction(self, query: str) -> bool:
        keywords = ["create", "alter", "show", "sys", "drop", "mysql", "insert"]
        query_keywords = query.lower().replace(".", " ").split(" ")
        to_restrict = 7 > len(set(keywords) - set(query_keywords))
        return to_restrict
