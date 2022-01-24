# import third party module


def test_create_connection(database_connections):
    # assert not connection_mysql.connection.closed, "mysql connection cannot be established"
    assert not database_connections[0].connection.closed, "postgresql connection cannot be established"
    assert not database_connections[1].connection.closed, "mssql connection cannot be established"


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
        # "SELECT * FROM students LIMIT 1",
        'SELECT * FROM "public"."FreeQuery" LIMIT 1',
        'SELECT TOP(1) * FROM [dbo].[AGENTS]'
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
