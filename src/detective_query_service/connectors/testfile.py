from detective_query_service.connectors.sql.my_sql import MySQLConnector

connection = MySQLConnector(
    host="sql11.freesqldatabase.com",
    user="sql11466052",
    password="nFpVm9qLtu",
    database="sql11466052"
)
print(connection.execute_query("SELECT * FROM students LIMIT 1"))
