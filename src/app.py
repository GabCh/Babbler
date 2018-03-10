import pymysql.cursors
from time import gmtime, strftime
import json
import os
from flask import Flask, render_template, request, session, url_for, redirect


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'babbler.db'),
    SECRET_KEY='dev key (change later)',
    USERNAME='admin',
    PASSWORD='NodesBand420!'
))

#  temp until DB is setup
users = [
    {
        'username': 'gablalib',
        'public_name': 'GabL',
        'password': ''
    }
]

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


@app.route('/')
def main():
    return render_template('index.html')



@app.route('/search')
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
        return render_template('/partials/search_results.html', keyword=keyword)
    else:
        return render_template('index.html')


@app.route('/login')
def login():
    view = render_template('partials/login.html')
    if request.method == 'POST':
        view = redirect(url_for('/'))
    return view


@app.route('/register')
def register():
    return render_template('/partials/register.html', users=users)  # TODO: get users from db


@app.route('/myprofile')
def profile():
    if session['logged_in']:
        return render_template('myprofile.html')
    else:
        return redirect(url_for('/login'))


if __name__ == '__main__':
    app.run()
