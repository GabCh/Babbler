import sqlite3


class BabblerDB(object):

    def __init__(self):
        self.db = sqlite3.connect('babbler.db')
        self.cursor = self.db.cursor()

    def create_table_babbler(self):
        sql = """
            CREATE TABLE babbler (
            Username VARCHAR(16) PRIMARY KEY,
            PublicName VARCHAR(16),
            Password VARCHAR(32)
            )
        """
        self.cursor.execute(sql)
