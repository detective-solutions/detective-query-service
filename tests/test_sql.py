

def test_create_connection(sql_database_connections):
    assert not sql_database_connections[0].connection.closed, "mysql connection cannot be established"
    assert not sql_database_connections[1].connection.closed, "mariadb connection cannot be established"
    assert not sql_database_connections[2].connection.closed, "postgresql connection cannot be established"
    assert not sql_database_connections[3].connection.closed, "mssql connection cannot be established"


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
            status = expected_result == conn.execute_query(query)[1]
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
            status = "error" not in query_result[1].keys()
        except IndexError:
            status = False

        results.append(status)

    assert all(results), "not all executable queries executed successfully"


def test_retrieve_tables_in_database(sql_database_connections, sql_database_setup_queries):
    pass
