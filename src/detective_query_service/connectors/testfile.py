"""
from detective_query_service.connectors.sql.sql_connector import SQLConnector


connection = SQLConnector(
    host="detective-azure-sql-server.database.windows.net",
    user="detective-server",
    password="iqPUjn9RPmcU9Qk",
    database="ms-sql-server-test",
    db_type="mssql"
)
print(connection.execute_query("SELECT TOP(1) * FROM [dbo].[AGENTS]"))
"""
import json
import requests

BASE = "http://127.0.0.1:5000/"
response = requests.get(BASE + "api/resource/ac83b5ca-7a2e-11ec-b7da-287fcf6e439d")
print(response.status_code)
print(response.json())

response2 = requests.post(BASE + "api/operation/", data=json.dumps({"query": "SELECT TOP(1) * FROM [dbo].[AGENTS]"}))
print(response2.json())

response = requests.get(BASE + "api/resource/ac83b5c9-7a2e-11ec-9da1-287fcf6e439d")
print(response.status_code)
print(response.json())

response2 = requests.post(BASE + "api/operation/", data=json.dumps({"query": 'SELECT * FROM "public"."FreeQuery" LIMIT 1'}))
print(response2.json())
