# import standard modules
from typing import Dict, List, Any, Tuple

# import third party modules
from sqlalchemy import text
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine, inspect

# import project related modules
from detective_query_service.log_definition import logger
from detective_query_service.transformers.tuples import tuple_to_json
from detective_query_service.connectors.general.connection import Connector
from detective_query_service.transformers.response import get_column_definitions


class SQLConnector(Connector):
    """
    This Connector is a wrapper around the SQLAlchemy Module from python wich provides access to most relational
    databases. With this Class comes support for:
     - Microsoft SQL Server
     - MySQL
     - MariaDB
     - Oracle
     - PostgreSQL
     One can easily use the class to connect to any of these databases by providing the following parameters:

     :param host: host-address
     :param user: username
     :param password: password related to user and database
     :param database: databse name
     :param port: port number as integer
     :param db_type: type of database as described above. Choose from (mssql, oracle, mysql and postgresql), (default - mysql)
    """

    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306,
                 db_type: str = "mysql", **kwargs):
        self.db_type = self._check_db_type_support(db_type)
        super().__init__(host, user, password, database, port)

    def __repr__(self):
        return f"SQLConnector: {self.db_type}"

    def _get_connection_string(self) -> str:
        """
        function to create the string of connection used by the engine. Since microsoft needs a
        special connection string it differs between mssql and other db_types provided at init level.

        :return: returns a connection address as string
        """
        base_connection_string = f"{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        if self.db_type == 'mssql':
            return f"{self.db_type}+pyodbc://{base_connection_string}?driver=ODBC+Driver+17+for+SQL+Server"
        else:
            return f"{self.db_type}://{base_connection_string}"

    def _check_db_type_support(self, db_type: str) -> str:
        """
        function to check whether a support for the provided db_type is given.

        :param db_type: string of provided type at init level must match (mysql, mariadb, postgresql, oracle mssql)
        :return: returns a db_type as string, mysql in case of error
        """
        supported = ['mysql', 'mariadb', 'postgresql', 'oracle', 'mssql']
        if db_type in supported:
            return db_type
        else:
            self.__error_status = f"{db_type} not supported, mysql driver is used as default"
            logger.error(self.__error_status)
            return 'mysql'

    def _create_connection(self) -> bool:
        """
        creates the engine and connection to a given database configuration

        :return: Ture if creating a connection was successful, False otherwise
        """
        try:
            engine = create_engine(
                self._get_connection_string(),
                echo=True, poolclass=NullPool
            )
            self.connection = engine.connect()
            return True

        except Exception as db_exception:
            self.__error_status = str(db_exception)
            logger.error(self.__error_status)
            return False

    def _query_restriction(self, query: str) -> bool:
        """
        function checks if the current query to execute does hold any mutation keywords or tries to access restricted
        values or to insert data.

        :param query: current query tried to be executed
        :return: True if a keyword to restrict is found, False otherwise
        """
        keywords = ["create", "alter", "show", "sys", "drop", "mysql", "insert", "admin"]
        query_keywords = query.lower().replace(".", " ").split(" ")
        to_restrict = any([x in query_keywords for x in keywords])
        return to_restrict

    def close(self):
        self.connection.close()

    def crawl_database(self, database_xid: str) -> dict:
        """
        creates a database snapshot of the connected source and database

        :param database_xid: dgraph xid identifier of the database
        :return: database connection details with table information
        """
        
        source_config = {
            "xid": database_xid,
            "host": self.host,
            "port": self.port,
            "db_type": self.db_type,
            "user": self.user,
            "password": self.password,
            "database": self.database
        }

        engine = self.connection
        inspector = inspect(self.connection)
        result = source_config
        result["tables"] = list()

        for table_name in inspector.get_table_names():
            schema = dict()
            schema["tableName"] = table_name
            schema["tableSchema"] = list()
            for column in inspector.get_columns(table_name):
                schema["tableSchema"].append(
                    {
                        "columnName": column["name"],
                        "columnType": str(column["type"])
                    }
                )
            result["tables"].append(schema)
        return result

    def execute_query(self, query: str) -> Tuple[List[Dict], Dict[str, Any]]:
        """
        executes a given query of selection operation for the created databse connection

        :param query: query string which needs to match the database syntax
        :return: a dict with key and list object
        """
        try:
            if self._query_restriction(query):
                logger.error(f"query tries to create, alter, show or use sys information: {query}")
                result = {"error": ["query tries to create, alter, show or use sys information"]}
            else:
                self._ensure_connection()

                t = text(f'''{query}''')
                query_result = self.connection.execute(t)
                result = query_result.fetchall()
                columns = query_result.keys()
                result = tuple_to_json(list(columns), result)

                if type(result) != dict:
                    logger.error(f"fetched result is not a list of tuples for: {query}")
                    result = {"error": ["not a valid query - fetched result is not a list of tuples"]}

            column_defs = get_column_definitions(result)
            return column_defs, result

        except Exception as db_exception:
            logger.error(str(db_exception))
            result = {"error": [str(db_exception)]}
            column_defs = get_column_definitions(result)
            return column_defs, result
