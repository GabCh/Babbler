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

    def read_table(self, table, keyword, attribute):
        sql = list()
        sql.append("SELECT * FROM %s " % table)
        sql.append("WHERE %s LIKE '%%%s%%'" % (attribute, keyword))
        sql.append(";")
        query = "".join(sql)
        cur = self.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return self.make_json_for_tuple(data)

    @staticmethod
    def make_json_for_tuple(data): # TODO: faire qu'elle fonctionne pour n'importe quelle table
        json = dict()
        json['babbles'] = []
        for tuple in data:
            babble = dict()
            babble['id'] = tuple[0]
            babble['pseudo'] = tuple[1]
            babble['message'] = tuple[2]
            babble['time_s'] = tuple[3]
            babble['tags'] = tuple[4]
            json['babbles'].append(babble)
        return json
