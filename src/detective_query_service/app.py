# import third party modules
from flask import Flask
from flask_restful import Api

# import project related modules
from detective_query_service.views import Database, DataQuery

app = Flask(__name__)
api = Api(app)

# define routes
api.add_resource(Database, "/api/resource/<string:uid>")
api.add_resource(DataQuery, "/api/operation/")


if __name__ == '__main__':
    app.run(debug=True)
