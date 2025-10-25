import sqlite3


class DatabaseConnection:
    def __enter__(self):
        self.conn = sqlite3.connect("database.db")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.conn.close()


with DatabaseConnection() as conn:
    ...
