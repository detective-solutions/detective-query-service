# import standard modules
import json
from typing import Any

# import third party modules
from flask import abort, request
from flask_restful import Resource

# import project related modules
from detective_query_service.log_definition import logger
from detective_query_service.settings import dgraph_client
from detective_query_service.graphql.databases import get_database_by_uid
from detective_query_service.connectors.general.standard import Connector

conn: Any = None
db_type: Any = None


class Database(Resource):
    def get(self, uid):
        try:
            db_config = get_database_by_uid(dgraph_client, uid)
            db_config = db_config["result"][0]
        except IndexError:
            abort(404, message="database id is not valid")

        try:
            global conn
            if conn is not None:
                conn.close()

            conn = Connector(**db_config)

            logger.info(f"connection established for {uid}")
            return {"info": f"connection established for {uid}"}

        except Exception as e:
            print(e, "error occured")
            return {"error": str(e)}


class DataQuery(Resource):
    def post(self):
        global conn
        try:
            query = json.loads(request.data)["query"]
            results = conn.execute_query(query)
            return {"data": results}

        except KeyError:
            abort(400, message="query not provided in payload")
