# import project related modules
from detective_query_service.connectors.sql.sql_connector import SQLConnector
from detective_query_service.connectors.mongodb.mongodb_connector import MongoDBConnector


def connector(db_type: str):
    """
    factory pattern selecting the right connector for a given database type

    SQL Variants
    - mySQL (mysql)
    - postgreSQL (postgresql)
    - MariaDB (mariadb)
    - Microsoft SQL Server (mssql)
    - Oracle DB (oracle)

    NO SQL Variants:
    - MongoDB

    :param db_type: descriping the data base type vailable patterns see above
    :return: Class Object of relevant connector
    """
    if db_type in ["mysql", "postgresql", "mariadb", "mssql", "oracle"]:
        return SQLConnector
    elif db_type == "mongodb":
        return MongoDBConnector
    else:
        return SQLConnector
