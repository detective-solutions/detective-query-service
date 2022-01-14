

class Connector:

    def __init__(self, host: str, user: str, password: str, database: str, port: int):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.error_status = None
        self.connection = None
        self.create_connection()
        print(self.error_status)

    def check_if_database_exist(self):
        return NotImplementedError

    def query_restriction(self, query: str) -> bool:
        return NotImplementedError

    def get_databases(self):
        return NotImplementedError

    def get_tables(self):
        return NotImplementedError

    def create_connection(self):
        return NotImplementedError

    def execute_query(self, query: str):
        return NotImplementedError
