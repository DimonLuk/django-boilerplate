class MockedConnection:
    def cursor(self):
        raise Exception
