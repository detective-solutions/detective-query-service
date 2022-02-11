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
            "table": "CREATE TABLE students (id serial PRIMARY KEY, name VARCHAR (20) UNIQUE NOT NULL);",
            "insert": "INSERT INTO students (id, name) VALUES (1, 'Sarah');",
            "test": "SELECT * FROM students LIMIT 1;"
        },
        "mssql": {
            "table": "CREATE TABLE testdb.students (id INT PRIMARY KEY IDENTITY (1, 1), name VARCHAR (20) NOT NULL);",
            "insert": "INSERT INTO testdb.students (id, name) VALUES (1, 'Sarah');",
            "test": "SELECT * FROM testdb.students LIMIT 1;"
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
            "port": 5432,
            "db_type": "postgresql"
        },
        "mssql": {
            "host": "0.0.0.0",
            "user": "sa",
            "password": "hsHlanZ0283819!lsH",
            "database": "testdb",
            "port": 1433,
            "db_type": "mssql"
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
def connection_msssql(database_configs):
    connection = SQLConnector(
        **database_configs.get("mssql", "mssql")
    )
    return connection


@pytest.fixture(scope="session")
def database_connections(connection_mysql, connection_postgresql, connection_msssql):
    return [
        connection_mysql,
        connection_postgresql,
        connection_msssql
    ]
