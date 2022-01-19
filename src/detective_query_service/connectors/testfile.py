from detective_query_service.connectors.sql.sql_connector import SQLConnector

connection = SQLConnector(
    host="dumbo.db.elephantsql.com",
    user="fkutbowf",
    password="6f8QOboUReqfLJ17mukRAyWBEME6xolU",
    database="fkutbowf",
    db_type="postgresql"
)

print(connection.execute_query('SELECT * FROM "public"."FreeQuery" LIMIT 1'))
