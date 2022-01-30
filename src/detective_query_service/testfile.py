from detective_query_service.connectors.mongodb.mongodb_connector import MongoDBConnector
import urllib.parse

conn = MongoDBConnector(
    host = "6funv",
    user = "test-user",
    password = "PnGrb8XiQG4iiEhy",
    cluster = "cluster0",
    database = "sample_airbnb"
)

print(conn.execute_query({"property_type": "Apartment"}, "listingsAndReviews"))