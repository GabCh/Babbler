from flask import Flask, render_template, request
import pymysql.cursors
from time import gmtime, strftime
import json

app = Flask(__name__)

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='minecraft371',
                             db='Babbler',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    # Create a new record
    sql = "INSERT INTO `babbles` (`id`, `pseudo`, `message`, `time_s`, `tags`) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (12345, 'blazeboy420', 'Test de babble',
                         strftime("%Y-%m-%d %H:%M:%S", gmtime()), json.dumps({"keyword": ["banane", "blaze"]})))

# connection is not autocommit by default. So you must commit to save
# your changes.
connection.commit()

with connection.cursor() as cursor:
    # Read a single record
    sql = "SELECT * FROM `babbles`"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)


@app.route("/")
def main():
    return render_template('app.html')


@app.route("/search")
def search_form():
    keyword = request.args.get('keyword')
    if keyword:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `babbles`"
                cursor.execute(sql)
                result = cursor.fetchall()
                print(result)
        finally:
            connection.close()
        return render_template('search_results.html', keyword=keyword)
    else:
        return render_template('search.html')


if __name__ == "__main__":
    app.run()
