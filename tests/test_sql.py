# import third party module
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData


def test_create_mysql_dummy_data(database_configs):
    config = database_configs.get("mysql", None)

    if config is not None:
        user = config.get("user", default="")
        password = config.get("password", default="")
        host = config.get("host", default="")
        port = config.get("port", default=3306)
        database = config.get("database", default="")

    test_engine = create_engine(f"mysql+mysqldb://{user}:{password}@{host}:{port}/{database}")
    data_available = False
    error = ""
    try:
        meta = MetaData()
        students = Table(
            'students', meta,
            Column('id', Integer, primary_key = True),
            Column('name', String),
            Column('lastname', String),
        )
        meta.create_all(test_engine)
        test_engine.execute("INSERT INTO students (id, name, lastname) VALUES (1, 'Sarah', 'Zauberbaum');")
        data_available = True
    except Exception as e:
        error = str(e)
    finally:
        assert data_available, f"{error}"


def test_create_connection(database_connections):
    assert not database_connections[0].connection.closed, "mysql connection cannot be established"
    # assert not database_connections[0].connection.closed, "postgresql connection cannot be established"
    # assert not connection_msssql.connection.closed, "mssql connection cannot be established"


def test_execute_query_with_restricted_values(database_connections):
    queries = [
        "CREATE DATABASE",
        "DROP TABLE IF EXISTS 'students'",
        "SHOW DATABASES",
        "SELECT User, Host, Password FROM mysql.user;",
        "ALTER MYDATABASE",
        "INSERT INTO `marks` (`id`, `student_id`, `mark`, `subject`) VALUES (35, 6, 88,  'Foreign Arts')"
    ]

    results = list()
    expected_result = {"error": ["query tries to create, alter, show or use sys information"]}
    for conn in database_connections:
        for query in queries:
            status = expected_result == conn.execute_query(query)
            results.append(status)

    assert all(results), "query with restricted values can be executed"


def test_execute_query_with_legitimate_values(database_connections):
    queries = [
        "SELECT * FROM testdb LIMIT 1",
        # 'SELECT * FROM "public"."FreeQuery" LIMIT 1',
        # 'SELECT TOP(1) * FROM [dbo].[AGENTS]'
    ]

    results = list()
    for ix, conn in enumerate(database_connections):
        print(queries[ix])
        try:
            query_result = conn.execute_query(queries[ix])
            status = "error" not in query_result.keys()
        except IndexError:
            status = False

        results.append(status)

    assert all(results), "not all executable queries executed successfully"
