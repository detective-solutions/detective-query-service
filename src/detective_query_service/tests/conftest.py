# import third party modules
import pytest

# import project related modules
from detective_query_service.connectors.sql.my_sql import MySQLConnector


@pytest.fixture(scope="session")
def mysql_test_connection():
    """
    create a connection with MySQLConnector to a remote dummy mysql database
        host: sql11.freesqldatabase.com
        login email: xkh27858@qopow.com
        database name and user name: sql11466052
        password: nFpVm9qLtu
    :return: mysql database connection
    """

    connection = MySQLConnector(
        host="sql11.freesqldatabase.com",
        user="sql11466052",
        password="nFpVm9qLtu",
        database="sql11466052"
    )

    return connection
