import os

from flask import Flask, render_template, request, session, url_for, redirect
from data.babblerdb import BabblerDB


app = Flask(__name__)
app.config.from_object(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'choupi'
app.config['MYSQL_DATABASE_DB'] = 'Babbler'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


#  temp until DB is setup
users = [
    {
        'username': 'gablalib',
        'public_name': 'GabL',
        'password': ''
    }
]

db = BabblerDB(app)
BABBLES_TABLE = 'babbles'
BABBLERS_TABLE = 'babblers'


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/search')
def search_form():
    keyword = request.args.get('keyword')
    if keyword:
        babbles = db.read_table(BABBLES_TABLE, keyword, 'message')
        babblers = db.read_table(BABBLERS_TABLE, keyword, 'PublicName')
        return render_template('/partials/search_results.html', keyword=keyword, babbles=babbles, babblers=babblers)
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

@app.route('/myfeed')
def feed():
    posts = [
        {
            "user": "Jannik",
            "time": "16h50",
            "message": "Salut tout le monde! :)",
            "tags": ["happy", "morning"]
        },
        {
            "user": "Choupi",
            "time": "16h25",
            "message": "Pour vrai tyl",
            "tags" : []
        },
        {
            "user": "Gabriel",
            "time": "16h21",
            "message": "!!!!!",
            "tags": ["Bring", "me", "food"]
        }
    ]
    return render_template('partials/feed.html', cards=posts)


if __name__ == '__main__':
    app.run()
