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
            keyword = '%' + keyword + '%'
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT username, message, time_s FROM {} WHERE {} LIKE %s".format(table, attribute)
                print(sql)
                cursor.execute(sql, (keyword,))
                results = cursor.fetchall()
                for result in results:
                    result['time_s'] = "{:%d %b %Y}".format(result['time_s'])
                return results
        except Exception as e:
            print(e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.connection.commit()
        finally:
            self.connection.close()
