# import third party module
import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


def get_connection_string(db_type, user, password, host, port, database):
    if db_type == 'mssql':
        return f"{db_type}+pyodbc://{user}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    else:
        return f"{db_type}://{user}:{password}@{host}:{port}/{database}"


@pytest.mark.parametrize("db_type", ["mysql", "postgresql", "mssql", "mariadb"])
def test_create_sql_dummy_data(sql_database_configs, sql_database_setup_queries, db_type):
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
        if db_type == "mssql":
            assert "testdb" in test_engine.url.database, "test db does not exist and was not created"

        test_conn = test_engine.connect()
        expected_result = [(1, "Sarah")]

        test_conn.execute(setup_queries["table"])
        test_conn.execute(setup_queries["insert"])
        test_result = test_conn.execute(setup_queries["test"]).fetchall()

        connection_status = test_conn.close
        test_conn.close()
        assert connection_status is not False, "no connection established"
        assert expected_result[0][1] == test_result[0][1], "db entry does not fit"
    else:
        assert config is not None, f"data base configuration for {db_type} not found"
        assert setup_queries is not None, f"database setup queries for {db_type} not found"


def test_create_connection(sql_database_connections):
    assert not sql_database_connections[0].connection.closed, "mysql connection cannot be established"
    assert not sql_database_connections[1].connection.closed, "postgresql connection cannot be established"
    assert not sql_database_connections[2].connection.closed, "mssql connection cannot be established"


def test_execute_query_with_restricted_values(sql_database_connections):
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
    for conn in sql_database_connections:
        for query in queries:
            status = expected_result == conn.execute_query(query)
            results.append(status)

    assert all(results), "query with restricted values can be executed"


def test_execute_query_with_legitimate_values(sql_database_connections, sql_database_setup_queries):
    queries = [
        values.get("test", "") for key, values in sql_database_setup_queries.items()
    ]

    results = list()
    for ix, conn in enumerate(sql_database_connections):
        print(queries[ix])
        try:
            query_result = conn.execute_query(queries[ix])
            status = "error" not in query_result.keys()
        except IndexError:
            status = False

        results.append(status)

    assert all(results), "not all executable queries executed successfully"
