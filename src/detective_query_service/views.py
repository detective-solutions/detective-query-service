# import standard modules
import json
from typing import Any

# import third party modules
from flask import abort, request
from flask_restful import Resource

# import project related modules
from detective_query_service.connectors.sql.sql_connector import SQLConnector


databases = {
    "ac83b5c8-7a2e-11ec-a95f-287fcf6e439d": {
        "host": "sql11.freesqldatabase.com",
        "user": "sql11466052",
        "password": "nFpVm9qLtu",
        "database": "sql11466052",
        "db_type": "mysql"
    },
    "ac83b5c9-7a2e-11ec-9da1-287fcf6e439d": {
        "host": "dumbo.db.elephantsql.com",
        "user": "fkutbowf",
        "password": "6f8QOboUReqfLJ17mukRAyWBEME6xolU",
        "database": "fkutbowf",
        "db_type": "postgresql"
    },
    "ac83b5ca-7a2e-11ec-b7da-287fcf6e439d": {
        "host": "detective-azure-sql-server.database.windows.net",
        "user": "detective-server",
        "password": "iqPUjn9RPmcU9Qk",
        "database": "ms-sql-server-test",
        "db_type": "mssql"
    }
}

conn: Any = None


def aboart_if_database_id_doesnt_exist(uid):
    if uid not in databases.keys():
        abort(404, message="database id is not valid...")


class Database(Resource):
    def get(self, uid):
        aboart_if_database_id_doesnt_exist(uid)
        try:
            global conn
            if conn is not None:
                conn.close()

            conn = SQLConnector(
                host=databases[uid]["host"],
                user=databases[uid]["user"],
                password=databases[uid]["password"],
                database=databases[uid]["database"],
                db_type=databases[uid]["db_type"]
            )
            return {"info": f"connection established for {uid}"}

        except Exception as e:
            print(e, "error occured")
            return {"error": str(e)}


class DataQuery(Resource):
    def post(self):
        global conn

        query = json.loads(request.data)["query"]
        results = conn.execute_query(query)

        return {"data": results}
