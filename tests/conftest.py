# import third party modules
import pytest

# import project related modules
from src.detective_query_service.connectors.sql.sql_connector import SQLConnector


@pytest.fixture(scope="session")
def sql_database_setup_queries():
    yield {
        "mysql": {
            "table": "CREATE TABLE students (id int, name varchar(20));",
            "insert": "INSERT INTO students (id, name) VALUES (1, 'Sarah');",
            "test": "SELECT * FROM students LIMIT 1;"
        },
        "mariadb": {
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
            "table": "CREATE TABLE students (id INT PRIMARY KEY, name VARCHAR (20) NOT NULL);",
            "insert": "INSERT INTO students (id, name) VALUES (1, 'Sarah');",
            "test": "SELECT TOP(1) * FROM students;"
        }

    }


@pytest.fixture(scope="session")
def sql_database_configs():
    yield {
        "mysql": {
            "host": "0.0.0.0",
            "user": "test_user",
            "password": "test",
            "database": "testdb",
            "port": 3306,
            "db_type": "mysql"
        },
        "mariadb": {
            "host": "0.0.0.0",
            "user": "test_user",
            "password": "test",
            "database": "testdb",
            "port": 3307,
            "db_type": "mariadb"
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
def connection_mysql(sql_database_configs):
    connection = SQLConnector(
        **sql_database_configs.get("mysql", "mysql")
    )
    return connection


@pytest.fixture(scope="session")
def connection_postgresql(sql_database_configs):
    connection = SQLConnector(
        **sql_database_configs.get("postgresql", "postgresql")
    )
    return connection


@pytest.fixture(scope="session")
def connection_msssql(sql_database_configs):
    connection = SQLConnector(
        **sql_database_configs.get("mssql", "mssql")
    )
    return connection


@pytest.fixture(scope="session")
def connection_mariadb(sql_database_configs):
    connection = SQLConnector(
        **sql_database_configs.get("mariadb", "mariadb")
    )
    return connection


@pytest.fixture(scope="session")
def sql_database_connections(
        connection_mysql,
        connection_mariadb,
        connection_postgresql,
        connection_msssql,

):
    return [
        connection_mysql,
        connection_mariadb,
        connection_postgresql,
        connection_msssql,
    ]


@pytest.fixture(scope="session")
def nosql_database_configs():
    yield {
        "mongodb": {
            "host": "0.0.0.0",
            "user": "test_user",
            "password": "test",
            "database": "testdb",
            "port": 27017,
            "db_type": "mysql"
        }
    }