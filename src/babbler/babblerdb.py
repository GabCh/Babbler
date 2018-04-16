import pymysql.cursors
from src.babbler.utils import get_elapsed_time


class BabblerDB(object):

    def __init__(self, app):
        self.connection = pymysql.connect(host=app.config['DB_HOST'],
                                          user=app.config['DB_USER'],
                                          password=app.config['DB_PASSWORD'],
                                          db=app.config['DB_NAME'],
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def add_babbler(self, username, publicName, password):
        sql = "INSERT INTO Babblers VALUES (%s , %s , %s)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (username, publicName, password))
                self.connection.commit()
        except Exception as e:
            print(e)

    def add_babble(self, id, username, message, time_s, tags):
        sql = "INSERT INTO Babbles VALUES (%s, %s, %s, %s, 0, 0)"
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

    def add_like(self, id, username):
        sql = "INSERT INTO Likes VALUES (%s, %s)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (id, username))
                self.connection.commit()
        except Exception as e:
            print(e)

    def add_comment_like(self, commentID, username):
        sql = "INSERT INTO CommentLikes VALUES (%s, %s)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (commentID, username))
                self.connection.commit()
        except Exception as e:
            print(e)

    def add_comment(self, babbleID, commentID, username, message, time_s):
        sql = "INSERT INTO Comments VALUES (%s, %s, %s, %s, %s, 0)"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (babbleID, commentID, username, message, time_s))
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
                    SELECT B.id, B.username, B.message, B.time_s, B.nbLikes, B.nbComments
                    FROM Babbles B, Follows F
                    WHERE F.follower LIKE %s AND F.followed = B.username OR B.username = %s
                    GROUP BY B.time_s DESC, B.username;"""
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

    def get_comments_of_babble(self, babbleID):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT B.commentID, B.username, B.message, B.time_s, nbLikes
                    FROM Comments B
                    WHERE B.babbleID = %s
                    GROUP BY B.time_s DESC, B.username;"""
                cursor.execute(sql, (babbleID,))
                results = cursor.fetchall()
                if not results:
                    return []
                for result in results:
                    result['time_s'] = "{}".format(result['time_s'])
                    result['elapsed'] = get_elapsed_time(result['time_s'])
                    #result['tags'] = self.read_tags(result['id'])
                return results
        except Exception as e:
            print(e)

    def generate_babble_id(self):
        sql = "SELECT MAX(id) AS max_id FROM Babbles"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                if result['max_id'] is None:
                    return 1
                else:
                    return result['max_id'] + 1
        except Exception as e:
            print(e)

    def generate_comment_id(self):
        sql = "SELECT MAX(commentID) AS max_id FROM Comments"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                if result['max_id'] is None:
                    return 1
                else:
                    return result['max_id'] + 1
        except Exception as e:
            print(e)

    def get_recent_babbles(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT B.id, B.username, B.message, B.time_s, B.nbLikes, B.nbComments
                FROM Babbles B
                ORDER BY B.time_s DESC
                LIMIT 100;"""

                cursor.execute(sql)
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

    def read_babbles(self, keyword: str):
        try:
            keyword = '%' + keyword + '%'
            with self.connection.cursor() as cursor:
                sql = "SELECT id, username, message, time_s, nbLikes, nbComments FROM Babbles WHERE message LIKE %s" \
                      "GROUP BY Babbles.time_s DESC, Babbles.username;"
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
                      "GROUP BY Babbles.time_s DESC, Babbles.username;"
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
                sql = "SELECT id, username, message, time_s, nbLikes, nbComments "\
                      "FROM Babbles WHERE username = %s" \
                      "GROUP BY Babbles.time_s DESC, Babbles.username;"
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

    def read_subscriptions(self, username: str):
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

    def remove_like(self, id, username):
        sql = "DELETE FROM Likes WHERE id = %s AND username = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (id, username))
                self.connection.commit()
        except Exception as e:
            print(e)

    def remove_comment_like(self, commentID, username):
        sql = "DELETE FROM CommentLikes WHERE id = %s AND username = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (commentID, username))
                self.connection.commit()
        except Exception as e:
            print(e)

    def remove_babble(self, id):
        sql = "DELETE FROM Babbles WHERE id = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (id,))
                self.connection.commit()
        except Exception as e:
            print(e)

    def remove_comment(self, commentID):
        sql = "DELETE FROM Comments WHERE commentID = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (commentID,))
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

    def already_liked_this_babble(self, id, username):
        sql = "SELECT username FROM Likes WHERE id = %s AND username = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (id, username))
                results = cursor.fetchall()
                if len(results) == 0:
                    return False
                else:
                    return True
        except Exception as e:
            print(e)

    def already_liked_this_comment(self, commentID, username):
        sql = "SELECT username FROM CommentLikes WHERE id = %s AND username = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (commentID, username))
                results = cursor.fetchall()
                if len(results) == 0:
                    return False
                else:
                    return True
        except Exception as e:
            print(e)

    def get_nbLikes(self, id):
        sql = "SELECT nbLikes FROM Babbles WHERE id = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (id,))
                result = cursor.fetchone()
                return result['nbLikes']
        except Exception as e:
            print(e)

    def get_comment_nbLikes(self, commentID):
        sql = "SELECT nbLikes FROM Comments WHERE commentID = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (commentID,))
                result = cursor.fetchone()
                return result['nbLikes']
        except Exception as e:
            print(e)

    def get_nbComments(self, id):
        sql = "SELECT nbComments FROM Babbles WHERE id = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (id,))
                result = cursor.fetchone()
                return result['nbComments']
        except Exception as e:
            print(e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.connection.commit()
        finally:
            self.connection.close()



