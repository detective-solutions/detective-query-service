# import third party modules
import pytest

# import project related modules
from src.detective_query_service.connectors.sql.sql_connector import SQLConnector


@pytest.fixture(scope="session")
def database_setup_queries():
    yield {
        "mysql": {
            "table": "CREATE TABLE students (id int, name varchar(20));",
            "insert": "INSERT INTO students (id, name) VALUES (1, 'Sarah');",
            "test": "SELECT * FROM students LIMIT 1;"
        },
        "postgresql": {
            "table": "CREATE TABLE students (id int, name varchar(20));",
            "insert": "INSERT INTO students (id, name) VALUES (1, 'Sarah');",
            "test": "SELECT * FROM students LIMIT 1;"
        }

    }


@pytest.fixture(scope="session")
def database_configs():
    yield {
        "mysql": {
            "host": "0.0.0.0",
            "user": "test_user",
            "password": "test",
            "database": "testdb",
            "port": 3306,
            "db_type": "mysql"
        },
        "postgresql": {
            "host": "0.0.0.0",
            "user": "test_user",
            "password": "test",
            "database": "testdb",
            "port": 8080,
            "db_type": "postgresql"
        }
    }


@pytest.fixture(scope="session")
def connection_mysql(database_configs):
    connection = SQLConnector(
        **database_configs.get("mysql", "mysql")
    )
    return connection


@pytest.fixture(scope="session")
def connection_postgresql(database_configs):
    connection = SQLConnector(
        **database_configs.get("postgresql", "postgresql")
    )
    return connection


# TODO: does not work on a ubuntu test instance in github actions, since ODBC driver is not installed by default
@pytest.fixture(scope="session")
def connection_msssql():
    """
    create a connection with MySQLConnector to a remote dummy mysql database
        host: dumbo.db.elephantsql.com
        database name and user name: fkutbowf
        password: 6f8QOboUReqfLJ17mukRAyWBEME6xolU
    :return: postgresql database connection
    """

    connection = SQLConnector(
        host="detective-azure-sql-server.database.windows.net",
        user="detective-server",
        password="iqPUjn9RPmcU9Qk",
        database="ms-sql-server-test",
        db_type="mssql"
    )

    return connection


@pytest.fixture(scope="session")
def database_connections(connection_mysql, connection_postgresql):
    return [
        connection_mysql,
        connection_postgresql
    ]
