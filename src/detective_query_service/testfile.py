

class InserTest:

    def __init__(self, host, name, number, **kwargs):
        self.host = host
        self.name = name
        self.number = number

    def show(self):
        print(self.host, self.name, self.number)


config = {"host": "website", "name": "peter", "number": 1, "palaba": "somting", "rambazambda": 2023}

it = InserTest(**config)
it.show()
