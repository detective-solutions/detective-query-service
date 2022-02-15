
from detective_query_service.connectors.sql.sql_connector import SQLConnector


query1 = '''
    SELECT *
    FROM pg_catalog.pg_tables
    WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';
    '''

query2 = '''SELECT * FROM "public"."FreeQuery" LIMIT 4'''
print(
    SQLConnector(
        host="dumbo.db.elephantsql.com",
        user="fkutbowf",
        password="6f8QOboUReqfLJ17mukRAyWBEME6xolU",
        database="fkutbowf",
        db_type="postgresql",
        port=5432
    ).execute_query('''SHOW DATABASES'''))
