import pymysql.cursors
from src.data.utils import get_elapsed_time


class BabblerDB(object):

    def __init__(self, app):
        self.connection = pymysql.connect(host=app.config['DB_HOST'],
                                          user=app.config['DB_USER'],
                                          password=app.config['DB_PASSWORD'],
                                          db=app.config['DB_NAME'],
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def add_babbler(self, username, publicName, password):
        sql = "INSERT INTO Babbler.Babblers VALUES ( %s , %s , %s)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (username, publicName, password))
                self.connection.commit()
        except Exception as e:
            print(e)

    def add_babble(self, id, username, message, time_s, tags):
        sql = "INSERT INTO Babbles VALUES (%s, %s, %s, %s)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (id, username, message, time_s))
                self.connection.commit()
                self.add_tags(id, tags)
        except Exception as e:
            print(e)

    def add_tags(self, babble_id, tags):
        for tag in tags:
            sql = "INSERT INTO Tag VALUES (%s, %s)"
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(sql, (babble_id, tag))
                    self.connection.commit()
            except Exception as e:
                print(e)

    def add_follower(self, follower, followed):
        sql = "INSERT INTO Follows VALUES (%s, %s)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (follower, followed))
                self.connection.commit()
        except Exception as e:
            print(e)

    def authenticate(self, username, password):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT username, publicName FROM Babblers WHERE username = %s AND password = %s"
                cursor.execute(sql, (username, password,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(e)

    def following(self, user: str, other: str):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT follower, followed FROM Follows WHERE follower = %s AND followed = %s"
                cursor.execute(sql, (user, other,))
                result = cursor.fetchone()
                if result:
                    return True
                else:
                    return False
        except Exception as e:
            print(e)

    def get_babbles_from_followed_babblers(self, username):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT B.id, B.username, B.message, B.time_s
                    FROM Babbles B, Follows F
                    WHERE F.follower LIKE %s AND F.followed = B.username OR B.username = %s
                    GROUP BY B.time_s DESC;"""
                cursor.execute(sql, (username, username,))
                results = cursor.fetchall()
                for result in results:
                    result['time_s'] = "{}".format(result['time_s'])
                    result['elapsed'] = get_elapsed_time(result['time_s'])
                    result['tags'] = self.read_tags(result['id'])
                if not results:
                    return []
                return results
        except Exception as e:
            print(e)

    def generate_babble_id(self):
        sql = "SELECT MAX(id) AS max_id FROM Babbles"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                return result['max_id'] + 1
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
                    result['elapsed'] = elapsed
                    result['tags'] = self.read_tags(result['id'])
                if results:
                    return results
                else:
                    return []
        except Exception as e:
            print(e)

    def read_babbles_with_tag(self, tag: str):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * "\
                      "FROM Babbles WHERE id IN (SELECT DISTINCT id FROM Tag WHERE tag = %s)" \
                      "GROUP BY Babbles.username, Babbles.time_s DESC;"
                cursor.execute(sql, (tag,))
                results = cursor.fetchall()
                for result in results:
                    result['time_s'] = "{}".format(result['time_s'])
                    elapsed = get_elapsed_time(result['time_s'])
                    result['elapsed'] = elapsed
                    result['tags'] = self.read_tags(result['id'])
                if results:
                    return results
                else:
                    return []
        except Exception as e:
            print(e)

    def read_user_babbles(self, username: str):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT id, username, message, time_s "\
                      "FROM Babbles WHERE username = %s" \
                      "GROUP BY Babbles.time_s DESC;"
                cursor.execute(sql, (username,))
                results = cursor.fetchall()
                for result in results:
                    result['time_s'] = "{}".format(result['time_s'])
                    elapsed = get_elapsed_time(result['time_s'])
                    result['elapsed'] = elapsed
                    result['tags'] = self.read_tags(result['id'])
                if results:
                    return results
                else:
                    return []
        except Exception as e:
            print(e)

    def read_tags(self, babble_id: int):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT DISTINCT tag FROM Tag WHERE id = %s"
                cursor.execute(sql, (babble_id,))
                results = cursor.fetchall()
                if results:
                    return results
                else:
                    return []
        except Exception as e:
            print(e)

    def read_babblers(self, username: str):
        try:
            keyword = '%' + username + '%'
            with self.connection.cursor() as cursor:
                sql = "SELECT username, publicName FROM Babblers WHERE username LIKE %s"
                cursor.execute(sql, (keyword,))
                results = cursor.fetchall()
                if results:
                    return results
                else:
                    return []
        except Exception as e:
            print(e)

    def read_followers(self, username: str):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT B.username, B.publicName FROM Babblers B
                    WHERE B.username IN
                    (SELECT F.followed FROM Follows F WHERE F.follower = %s);
                      """
                cursor.execute(sql, (username,))
                results = cursor.fetchall()
                if results:
                    return results
                else:
                    return []
        except Exception as e:
            print(e)

    def read_subscriptions(self, username: str):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT B.username, B.publicName FROM Babblers B
                    WHERE B.username IN
                    (SELECT F.follower FROM Follows F WHERE F.followed = %s);
                      """
                cursor.execute(sql, (username,))
                results = cursor.fetchall()
                if results:
                    return results
                else:
                    return []
        except Exception as e:
            print(e)

    def remove_follower(self, follower, followed):
        sql = "DELETE FROM Follows WHERE follower = %s AND followed = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (follower, followed))
                self.connection.commit()
        except Exception as e:
            print(e)

    def remove_babbler(self, username):
        sql = "DELETE FROM Babblers WHERE username = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (username,))
                self.connection.commit()
        except Exception as e:
            print(e)

    def validate_username(self, username):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT username FROM Babblers WHERE username = %s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.connection.commit()
        finally:
            self.connection.close()



