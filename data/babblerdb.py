from flaskext.mysql import MySQL
import json


class BabblerDB(object):

    def __init__(self, app):
        self.mysql = MySQL()
        self.mysql.init_app(app)
        self.connection = self.mysql.connect()
        self.cursor = self.connection.cursor()
        sql = list()
        sql.append("USE Babbler;")
        query = "".join(sql)
        self.connection.cursor().execute(query)

    def create_table_babblers(self):
        sql = """
            CREATE TABLE babblers (
            Username VARCHAR(16) PRIMARY KEY,
            PublicName VARCHAR(16),
            Password VARCHAR(32)
            );
        """
        self.cursor.execute(sql)
        print('Created babblers table!')

    def add_babbler(self, username, public_name, password):
        sql = """
            INSERT INTO babblers (Username, PublicName, Password)
            VALUES (""" + username + ',' + public_name + ',' + password + ');'
        self.cursor.execute(sql)
        print('Inserted ' + username + ' into table babblers!')

    def read(self, table, keyword, attribute):
        sql = list()
        sql.append("SELECT * FROM %s " % table)
        sql.append("WHERE %s LIKE '%%%s'" % (attribute, keyword))
        sql.append(";")
        query = "".join(sql)
        cur = self.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return json.JSONEncoder().encode(data) # TODO make json valid for templating

    def delete(self, table, **kwargs):
        sql = list()
        sql.append("DELETE FROM %s " % table)
        sql.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in kwargs.items()))
        sql.append(";")
        query = "".join(sql)
        return self.cursor.execute(query)
