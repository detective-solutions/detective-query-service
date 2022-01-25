from detective_query_service.connectors.sql.sql_connector import SQLConnector

connection = SQLConnector(
    host="sql11.freesqldatabase.com",
    user="sql11466052",
    password="nFpVm9qLtu",
    database="sql11466052",
    db_type="mysql"
)

print(connection.connection.closed)