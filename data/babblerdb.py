import pymysql.cursors


class BabblerDB(object):

    def __init__(self, app):
        self.connection = pymysql.connect(host=app.config['DB_HOST'],
                                          user=app.config['DB_USER'],
                                          password=app.config['DB_PASSWORD'],
                                          db=app.config['DB_NAME'],
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

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
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM %s WHERE %s LIKE '%%%s%%'"
                cursor.execute(sql, (table, attribute, keyword,))
                result = cursor.fetchall()
                print(result)
                return self.make_json_for_tuple(result)
        finally:
            self.connection.close()

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
