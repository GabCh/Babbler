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

    def add_babbler(self, username, publicName, password):
        sql = """
            INSERT INTO Babblers (username, publicName, password)
            VALUES ( %s , %s , %s);"""
        #try:
            #self.cursor.execute(sql, (username, publicName, password))
        print('Inserted ' + username + ' into table babblers!')

    def add_babble(self, id, username, message, time_s, tags):
        sql = """
            INSERT INTO Babbles (id, username, message, time_s)
            VALUES (%s, %s, %s, %s);"""
        self.cursor.execute(sql, (id, username, message, time_s))
        self.add_tags(id, tags)

    def add_tags(self, id, tags):
        for t in tags:
            sql = """
                INSERT INTO Tag (id, tag)
                VALUES (%s, %s);"""
            self.cursor.execute(sql, (id, t))

    def add_follower(self, follower, followed):
        sql = """
            INSERT INTO Follows (follower, followed)
            VALUES (%s, %s);"""
        self.cursor.execute(sql, (follower, followed))

    def read_table(self, table, keyword, attribute):
        sql = list()
        sql.append("SELECT * FROM %s ", (table,))
        sql.append("WHERE %s LIKE '%%%s%%'", (attribute, keyword))
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
