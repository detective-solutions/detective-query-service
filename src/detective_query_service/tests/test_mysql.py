# import project related modules
from detective_query_service.tests.conftest import mysql_test_connection


def test_create_connection(self, mysql_test_connection):
    self.assertTrue(mysql_test_connection.connection.is_connected(), True)


def test_execute_query_with_restricted_values(self, mysql_test_connection):
    queries = [
        "CREATE DATABASE",
        "DROP TABLE IF EXISTS 'students'",
        "SHOW DATABASES",
        "SELECT User, Host, Password FROM mysql.user;",
        "ALTER MYDATABASE",
        "INSERT INTO `marks` (`id`, `student_id`, `mark`, `subject`) VALUES (35, 6, 88,  'Foreign Arts')"
    ]

    results = list()
    for query in queries:
        status = "error" == mysql_test_connection.execute_query(query)[0][0]
        results.append(status)

    self.assertTrue(all(results))


def test_execute_query_with_legitimate_values(self, mysql_test_connection):
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

    self.assertTrue(all(results))
