# import standard modules
import json
from typing import Any

# import third party modules
from flask import abort, request
from flask_restful import Resource

# import project related modules
from detective_query_service.settings import dgraph_client, logger
from detective_query_service.graphql.databases import get_database_by_xid
from detective_query_service.connectors.sql.sql_connector import SQLConnector

conn: Any = None


class Database(Resource):
    def get(self, uid):
        try:
            db_config = get_database_by_xid(dgraph_client, uid)
            db_config = db_config["result"][0]
        except IndexError:
            abort(404, message="database id is not valid")

        try:
            global conn
            if conn is not None:
                conn.close()

            conn = SQLConnector(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["database"],
                db_type=db_config["db_type"]
            )

            logger.info(f"connection established for {uid}")
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
