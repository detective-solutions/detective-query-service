
def test_create_connection(mysql_test_connection):
    assert not mysql_test_connection.connection.closed, "connection cannot be established"


def test_execute_query_with_restricted_values(mysql_test_connection):
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
    for query in queries:
        status = expected_result == mysql_test_connection.execute_query(query)
        results.append(status)

    assert all(results), "query with restricted values can be executed"


def test_execute_query_with_legitimate_values(mysql_test_connection):
    queries = [
        "SELECT * FROM students LIMIT 1"
    ]

    results = list()
    for query in queries:
        try:
            status = "error" != mysql_test_connection.execute_query(query)[0][0]
        except IndexError:
            status = False

        results.append(status)

    assert all(results), "not all executable queries executed successfully"
