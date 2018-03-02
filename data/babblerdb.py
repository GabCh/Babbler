from flaskext.mysql import MySQL


class BabblerDB(object):

    def __init__(self, app):
        self.mysql = MySQL()
        self.mysql.init_app(app)
        self.cursor = self.mysql.get_db().cursor()

    def create_table_babblers(self):
        sql = """
            CREATE TABLE babblers (
            Username VARCHAR(16) PRIMARY KEY,
            PublicName VARCHAR(16),
            Password VARCHAR(32)
            )
        """
        self.cursor.execute(sql)
