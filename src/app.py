import os

from flask import Flask, render_template, request, session, url_for, redirect
from data.babblerdb import BabblerDB


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE_URI='mysql://root@localhost/Babbler',
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
        babbles = db.read(BABBLES_TABLE, keyword, 'message')
        babblers = db.read(BABBLERS_TABLE, keyword, 'PublicName')
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


if __name__ == '__main__':
    app.run()
