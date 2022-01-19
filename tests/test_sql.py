# import third party module


def test_create_connection(connection_mysql, connection_postgresql):
    assert not connection_mysql.connection.closed, "mysql connection cannot be established"
    assert not connection_postgresql.connection.closed, "postgresql connection cannot be established"


def test_execute_query_with_restricted_values(connection_mysql, connection_postgresql):
    queries = [
        "CREATE DATABASE",
        "DROP TABLE IF EXISTS 'students'",
        "SHOW DATABASES",
        "SELECT User, Host, Password FROM mysql.user;",
        "ALTER MYDATABASE",
        "INSERT INTO `marks` (`id`, `student_id`, `mark`, `subject`) VALUES (35, 6, 88,  'Foreign Arts')"
    ]

    results = list()
    expected_result = [("error", "query tries to create, alter, show or use sys information")]
    for conn in [connection_mysql, connection_postgresql]:
        for query in queries:
            status = expected_result == conn.execute_query(query)
            results.append(status)

    assert all(results), "query with restricted values can be executed"


def test_execute_query_with_legitimate_values(connection_mysql, connection_postgresql):
    queries = [
        "SELECT * FROM students LIMIT 1",
        'SELECT * FROM "public"."FreeQuery" LIMIT 1'
    ]

    results = list()
    conns = [connection_mysql, connection_postgresql]
    for ix, conn in enumerate(conns):
        print(queries[ix])
        try:
            status = "error" != conn.execute_query(queries[ix])[0][0]
        except IndexError:
            status = False

        results.append(status)

    assert all(results), "not all executable queries executed successfully"
