# import third party modules
import pytest

# import project related modules
from src.detective_query_service.connectors.sql.sql_connector import SQLConnector


@pytest.fixture(scope="session")
def connection_mysql():
    """
    create a connection with MySQLConnector to a remote dummy mysql database
        host: sql11.freesqldatabase.com
        login email: xkh27858@qopow.com
        database name and user name: sql11466052
        password: nFpVm9qLtu
    :return: mysql database connection
    """

    connection = SQLConnector(
        host="mysql-master",
        user="root",
        password="root",
        database="test",
        db_type="mysql"
    )

    return connection


@pytest.fixture(scope="session")
def connection_postgresql():
    """
    create a connection with MySQLConnector to a remote dummy mysql database
        host: dumbo.db.elephantsql.com
        database name and user name: fkutbowf
        password: 6f8QOboUReqfLJ17mukRAyWBEME6xolU
    :return: postgresql database connection
    """

    connection = SQLConnector(
        host="dumbo.db.elephantsql.com",
        user="fkutbowf",
        password="6f8QOboUReqfLJ17mukRAyWBEME6xolU",
        database="fkutbowf",
        db_type="postgresql"
    )

    return connection


# TODO: does not work on a ubuntu test instance in github actions, since ODBC driver is not installed by default
@pytest.fixture(scope="session")
def connection_msssql():
    """
    create a connection with MySQLConnector to a remote dummy mysql database
        host: dumbo.db.elephantsql.com
        database name and user name: fkutbowf
        password: 6f8QOboUReqfLJ17mukRAyWBEME6xolU
    :return: postgresql database connection
    """

    connection = SQLConnector(
        host="detective-azure-sql-server.database.windows.net",
        user="detective-server",
        password="iqPUjn9RPmcU9Qk",
        database="ms-sql-server-test",
        db_type="mssql"
    )

    return connection


@pytest.fixture(scope="session")
def database_connections(connection_mysql):
    return [
        # connection_postgresql
        connection_mysql
    ]
