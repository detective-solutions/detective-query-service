from detective_query_service.connectors.sql.sql_connector import SQLConnector

connection = SQLConnector(
    host="detective-azure-sql-server.database.windows.net",
    user="detective-server",
    password="iqPUjn9RPmcU9Qk",
    database="ms-sql-server-test",
    db_type="mssql"
)

print(connection.connection.closed)