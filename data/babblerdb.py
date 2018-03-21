import pymysql.cursors


class BabblerDB(object):

    def __init__(self, app):
        self.connection = pymysql.connect(host=app.config['DB_HOST'],
                                          user=app.config['DB_USER'],
                                          password=app.config['DB_PASSWORD'],
                                          db=app.config['DB_NAME'],
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def add_babbler(self, username, public_name, password):
        sql = """
            INSERT INTO babblers (Username, PublicName, Password)
            VALUES (""" + username + ',' + public_name + ',' + password + ');'
        self.cursor.execute(sql)
        print('Inserted ' + username + ' into table babblers!')

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
