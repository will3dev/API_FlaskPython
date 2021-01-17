import sqlite3

class DatabaseConnection:
    def __init__(self, host):
        self.host = host
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.host)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.connection.closer()
        else:
            self.connection.committ()
            self.connection.close()