import pymysql.cursors
from data.utils import get_elapsed_time


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
        try:
            with self.connection.cursor() as cursor:
                self.cursor.execute(sql, (username, publicName, password))
        except Exception as e:
            print(e)
        print('Inserted ' + username + ' into table babblers!')

    def add_babble(self, id, username, message, time_s, tags):
        sql = """
            INSERT INTO Babbles (id, username, message, time_s)
            VALUES (%s, %s, %s, %s);"""
        try:
            with self.connection.cursor() as cursor:
                self.cursor.execute(sql, (id, username, message, time_s))
        except Exception as e:
            print(e)
        self.add_tags(id, tags)

    def add_tags(self, id, tags):
        for t in tags:
            sql = """
                INSERT INTO Tag (id, tag)
                VALUES (%s, %s);"""
            try:
                with self.connection.cursor() as cursor:
                    self.cursor.execute(sql, (id, t))
            except Exception as e:
                print(e)

    def add_follower(self, follower, followed):
        sql = """
            INSERT INTO Follows (follower, followed)
            VALUES (%s, %s);"""
        try:
            with self.connection.cursor() as cursor:
                self.cursor.execute(sql, (follower, followed))
        except Exception as e:
            print(e)

    def read_babbles(self, keyword: str):
        try:
            keyword = '%' + keyword + '%'
            with self.connection.cursor() as cursor:
                sql = "SELECT id, username, message, time_s FROM Babbles WHERE message LIKE %s" \
                      "GROUP BY Babbles.time_s DESC;"
                cursor.execute(sql, (keyword,))
                results = cursor.fetchall()
                for result in results:
                    result['time_s'] = "{}".format(result['time_s'])
                    elapsed = get_elapsed_time(result['time_s'])
                    result['ellapsed'] = elapsed
                    result['tags'] = self.read_tags(result['id'])
                return results
        except Exception as e:
            print(e)

    def read_babbles_with_tag(self, tag: str):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT id, username, message, time_s "\
                      "FROM Babbles WHERE id IN (SELECT id FROM Tag WHERE tag = %s)" \
                      "GROUP BY Babbles.time_s DESC;"
                cursor.execute(sql, (tag,))
                results = cursor.fetchall()
                for result in results:
                    result['time_s'] = "{}".format(result['time_s'])
                    elapsed = get_elapsed_time(result['time_s'])
                    result['ellapsed'] = elapsed
                    result['tags'] = self.read_tags(result['id'])
                return results
        except Exception as e:
            print(e)

    def read_tags(self, babble_id: int):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT DISTINCT tag FROM Tag WHERE id = %s"
                cursor.execute(sql, (babble_id,))
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(e)

    def read_babblers(self, username: str):
        try:
            keyword = '%' + username + '%'
            with self.connection.cursor() as cursor:
                sql = "SELECT username, publicName FROM Babblers WHERE username LIKE %s"
                cursor.execute(sql, (keyword,))
                results = cursor.fetchall()
                return results
        except Exception as e:
            print(e)

    def get_babbles_from_followed_babblers(self, username):
        try:
            username = '%' + username + '%'
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT B.username, B.message, B.time_s
                    FROM Babbles B, Follows F
                    WHERE F.follower LIKE %s AND F.followed = B.username
                    GROUP BY B.time_s DESC;"""
                cursor.execute(sql, (username,))
                results = cursor.fetchall()
                for result in results:
                    result['time_s'] = "{}".format(result['time_s'])
                    result['ellapsed'] = get_elapsed_time(result['time_s'])
                return results
        except Exception as e:
            print(e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.connection.commit()
        finally:
            self.connection.close()



