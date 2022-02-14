# import third party modules
import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

# import project related modules
from src.detective_query_service.connectors.general.factory import connector


def get_connection_string(db_type, user, password, host, port, database):
    if db_type == 'mssql':
        return f"{db_type}+pyodbc://{user}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    else:
        return f"{db_type}://{user}:{password}@{host}:{port}/{database}"


def create_sql_dummy_data(sql_database_configs, sql_database_setup_queries, db_type):
    config = sql_database_configs.get(db_type, None)
    setup_queries = sql_database_setup_queries.get(db_type, None)

    if (config is not None) and (setup_queries is not None):
        user = config.get("user", "")
        password = config.get("password", "")
        host = config.get("host", "")
        port = config.get("port", 3306)
        database = config.get("database", "")

        connection_string = get_connection_string(db_type, user, password, host, port, database)
        test_engine = create_engine(connection_string)
        if not database_exists(test_engine.url):
            create_database(test_engine.url)

        test_conn = test_engine.connect()
        expected_result = [(1, "Sarah")]

        test_conn.execute(setup_queries["table"])
        test_conn.execute(setup_queries["insert"])
        test_result = test_conn.execute(setup_queries["test"]).fetchall()

        connection_status = test_conn.close
        test_conn.close()
        assert connection_status is not False, "no connection established"
        assert expected_result[0][1] == test_result[0][1], "db entry does not fit"
        return True
    else:
        assert config is not None, f"data base configuration for {db_type} not found"
        assert setup_queries is not None, f"database setup queries for {db_type} not found"
        return False


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
def connection_mysql(sql_database_configs, sql_database_setup_queries):
    error_msg = "mysql database could not be created"
    assert create_sql_dummy_data(sql_database_configs, sql_database_setup_queries, "mysql"), error_msg
    conn = connector("mysql")
    connection = conn(
        **sql_database_configs["mysql"]
    )
    return connection


@pytest.fixture(scope="session")
def connection_mariadb(sql_database_configs, sql_database_setup_queries):
    error_msg = "mariadb database could not be created"
    assert create_sql_dummy_data(sql_database_configs, sql_database_setup_queries, "mariadb"), error_msg
    conn = connector("mariadb")
    connection = conn(
        **sql_database_configs["mariadb"]
    )
    return connection


@pytest.fixture(scope="session")
def connection_postgresql(sql_database_configs, sql_database_setup_queries):
    error_msg = "postgresql database could not be created"
    assert create_sql_dummy_data(sql_database_configs, sql_database_setup_queries, "postgresql"), error_msg
    conn = connector("postgresql")
    connection = conn(
        **sql_database_configs["postgresql"]
    )
    return connection


@pytest.fixture(scope="session")
def connection_msssql(sql_database_configs, sql_database_setup_queries):
    error_msg = "mssql database could not be created"
    assert create_sql_dummy_data(sql_database_configs, sql_database_setup_queries, "mssql"), error_msg
    conn = connector("mssql")
    connection = conn(
        **sql_database_configs["mssql"]
    )
    return connection


@pytest.fixture(scope="session")
def sql_database_connections(
        connection_mysql,
        connection_mariadb,
        connection_postgresql,
        connection_msssql

):
    return [
        connection_mysql,
        connection_mariadb,
        connection_postgresql,
        connection_msssql
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
            "db_type": "mongodb"
        }
    }


@pytest.fixture(scope="session")
def nosql_database_setup_queries():
    yield {
        "mongodb": {
            "table": "CREATE TABLE students (id int, name varchar(20));",
            "insert": "INSERT INTO students (id, name) VALUES (1, 'Sarah');",
            "test": "SELECT * FROM students LIMIT 1;"
        }
    }


@pytest.fixture(scope="session")
def connection_mongodb(nosql_database_configs):
    conn = connector("mongodb")
    connection = conn(
        **nosql_database_configs.get("mongodb", "mongodb")
    )
    return connection


@pytest.fixture(scope="session")
def nosql_database_connections(
        connection_mongodb
):
    return [
        connection_mongodb
    ]
