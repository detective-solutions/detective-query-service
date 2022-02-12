# import standard modules
import urllib
from sys import platform

# import third party module
import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


def get_connection_string(db_type, user, password, host, port, database):
    if db_type == 'mssql':
        return f"{db_type}+pyodbc://{user}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server?ssl=true"
    else:
        return f"{db_type}://{user}:{password}@{host}:{port}/{database}"


@pytest.mark.parametrize("db_type", ["mysql", "postgresql", "mssql"])
def test_create_sql_dummy_data(database_configs, database_setup_queries, db_type):
    config = database_configs.get(db_type, None)
    setup_queries = database_setup_queries.get(db_type, None)

    if (config is not None) and (setup_queries is not None):
        user = config.get("user", "")
        password = config.get("password", "")
        host = config.get("host", "")
        port = config.get("port", 3306)
        database = config.get("database", "")

        connection_string = get_connection_string(db_type, user, password, host, port, database)
        test_engine = create_engine(connection_string)
        if (db_type != "mssql") and (not database_exists(test_engine.url)):
            create_database(test_engine.url)
        else:
            test_engine.execute(f"CREATE DATABASE {database}")

        test_conn = test_engine.connect()
        expected_result = [(1, "Sarah")]

        test_engine.execute(setup_queries["table"])
        test_conn.execute(setup_queries["insert"])
        test_result = test_conn.execute(setup_queries["test"]).fetchall()

        connection_status = test_conn.close
        test_conn.close()
        assert connection_status is not False, "no connection established"
        assert expected_result[0][1] == test_result[0][1], "db entry does not fit"
    else:
        assert config is not None, f"data base configuration for {db_type} not found"
        assert setup_queries is not None, f"database setup queries for {db_type} not found"


def test_create_connection(database_connections):
    assert not database_connections[0].connection.closed, "mysql connection cannot be established"
    assert not database_connections[1].connection.closed, "postgresql connection cannot be established"
    assert not database_connections[2].connection.closed, "mssql connection cannot be established"


def test_execute_query_with_restricted_values(database_connections):
    queries = [
        "CREATE DATABASE",
        "DROP TABLE IF EXISTS 'students'",
        "SHOW DATABASES",
        "SELECT User, Host, Password FROM mysql.user;",
        "ALTER MYDATABASE",
        "INSERT INTO `marks` (`id`, `student_id`, `mark`, `subject`) VALUES (35, 6, 88,  'Foreign Arts')"
    ]

    results = list()
    expected_result = {"error": ["query tries to create, alter, show or use sys information"]}
    for conn in database_connections:
        for query in queries:
            status = expected_result == conn.execute_query(query)
            results.append(status)

    assert all(results), "query with restricted values can be executed"


def test_execute_query_with_legitimate_values(database_connections):
    queries = [
        'SELECT * FROM students LIMIT 1',
        'SELECT * FROM students LIMIT 1',
        # 'SELECT TOP(1) * FROM [dbo].[AGENTS]'
    ]

    results = list()
    for ix, conn in enumerate(database_connections):
        print(queries[ix])
        try:
            query_result = conn.execute_query(queries[ix])
            status = "error" not in query_result.keys()
        except IndexError:
            status = False

        results.append(status)

    assert all(results), "not all executable queries executed successfully"
