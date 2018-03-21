import pymysql.cursors
from data.utils import get_elapsed_time, get_total_seconds


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

    def read_babbles(self, keyword):
        try:
            keyword = '%' + keyword + '%'
            with self.connection.cursor() as cursor:
                sql = "SELECT username, message, time_s FROM Babbles WHERE message LIKE %s"
                cursor.execute(sql, (keyword,))
                results = cursor.fetchall()
                for result in results:
                    result['time_s'] = "{}".format(result['time_s'])
                    elapsed = get_elapsed_time(result['time_s'])
                    seconds = get_total_seconds(result['time_s'])
                    result['ellapsed'] = elapsed
                    result['seconds'] = seconds
                chrono = sorted(results, key=lambda k: k['seconds'])
                return chrono
        except Exception as e:
            print(e)

    def read_babblers(self, username):
        try:
            keyword = '%' + username + '%'
            with self.connection.cursor() as cursor:
                sql = "SELECT username, publicName FROM Babblers WHERE username LIKE %s"
                cursor.execute(sql, (keyword,))
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.connection.commit()
        finally:
            self.connection.close()
