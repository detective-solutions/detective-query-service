
import pyodbc
print([x for x in pyodbc.drivers()])
"""
mssql:
image: mcr.microsoft.com/mssql/server:2019-latest
ports:
- 1433:1433
env:
MSSQL_DATABASE: ${{ env.SQL_DATABASE }}
MSSQL_USER: ${{ env.SQL_USER }}
MSSQL_PASSWORD: ${{ env.SQL_PASSWORD }}
MSSQL_ROOT_PASSWORD: ${{ env.SQL_PASSWORD }}
"""
