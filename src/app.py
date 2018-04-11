import hashlib
import binascii
import datetime
import os
import shutil

from flask import Flask, render_template, request, session, redirect
from src.babbler.babblerdb import BabblerDB
from src.babbler.utils import crop_tags_in_message


app = Flask(__name__)
app.config.from_object(__name__)

# By default in Flask, session expires after 31 days.
app.secret_key = 'YmxhemVpdDQyMA=='

# Config data for DB
app.config['DB_HOST'] = 'localhost'
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = 'babblerisawesome'
app.config['DB_NAME'] = 'Babbler'
db = BabblerDB(app)

#  Hashing salt
salt = '1WZZhonPwvMWzu3pU5J+4fp1d9SCHYi3qQ4QpxTvznatMsSzl4iOKCtF++vBJ+ZQPOXCDIs0ipiaPAlEI2RSGQ=='


@app.route('/')
def main():
    logged = 'username' in session
    if logged:
        username = session['username']
        babbles = db.get_babbles_from_followed_babblers(username)
        return render_template('index.html',
                               new_login=request.args.get('new_login'),
                               babbler=username, babbles=babbles,
                               logged=logged)
    else:
        return redirect('/login')


@app.route('/new-babble', methods=['GET', 'POST'])
def new_babble():
    if 'username' in session:
        if request.method == 'POST':
            data = request.form
            message = data['babble']
            tags, message = crop_tags_in_message(message)
            id = db.generate_babble_id()
            db.add_babble(id, session['username'], message, datetime.datetime.now(), tags)
            return redirect('/myfeed')
        else:
            return render_template('/partials/newbabble.html', logged=True)
    else:
        return redirect('/login')


@app.route('/delete/<user>', methods=['GET', 'POST'])
def delete(user):
    connected_user = 'username' in session
    if request.method == 'POST':
        if connected_user and session['username'] == user:
            session.pop('username', None)
            db.remove_babbler(user)
            os.remove('./static/images/' + str(user) + '.jpg')
            return redirect('/login')
    else:
        return render_template('/partials/delete_user.html', user=user, logged=True)


@app.route('/follow/<other>', methods=['POST'])
def follow(other):
    if 'username' in session:
        db.add_follower(session['username'], other)
        return redirect('/babblers/' + str(other))


@app.route('/unfollow/<other>', methods=['POST'])
def unfollow(other):
    if 'username' in session:
        db.remove_follower(session['username'], other)
        return redirect('/babblers/' + str(other))


@app.route('/login', methods=['GET', 'POST'])
def login():
    view = render_template('/partials/login.html',
                           newly_registered=request.args.get('newly_registered'),
                           invalid=request.args.get('invalid'))
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = hashlib.pbkdf2_hmac('sha256', data['password'].encode(), salt.encode(), 65336)
        password = str(binascii.hexlify(password))[2:-1]

        result = db.authenticate(username, password)
        if result:
            session['username'] = username
            session['publicName'] = result['publicName']
            return 'True'
    return view


@app.route('/register', methods=['GET', 'POST'])
def register():
    view = render_template('/partials/register.html')
    if request.method == 'POST':
        data = request.form
        password = hashlib.pbkdf2_hmac('sha256', data['password'].encode(), salt.encode(), 65336)
        password = str(binascii.hexlify(password))[2:-1]
        db.add_babbler(data['username'], data['public_name'], password)
        shutil.copy(os.path.abspath('static/placeholders/profile.jpg'),
                    os.path.abspath('static/images/' + str(data['username']) + '.jpg'))
    return view


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


@app.route('/myprofile')
def my_profile():
    if 'username' in session:
        user = {'username': session['username'], 'publicName': session['publicName']}
        babbles = db.read_user_babbles(user['username'])
        followers = db.read_followers(user['username'])
        subscriptions = db.read_subscriptions(user['username'])
        followed = db.following(session['username'], user['username'])
        nb_babbles = len(babbles)
        nb_followers = len(followers)
        nb_subscriptions = len(subscriptions)
        view = render_template('/partials/myprofile.html', user=user,
                               followed=followed, babbles=babbles, logged=True,
                               followers=followers, subscriptions=subscriptions,
                               nb_babbles=nb_babbles, nb_followers=nb_followers,
                               nb_subscriptions=nb_subscriptions)
        return view
    else:
        return redirect('/login')


@app.route('/myfeed')
def feed():
    if 'username' in session:
        babbles = db.get_babbles_from_followed_babblers(session['username'])
        return render_template('/partials/myfeed.html', babbles=babbles, logged=True)
    else:
        return redirect('/login')


@app.route('/babblers/<username>')
def babbler_profile(username):
    if 'username' in session:
        if session['username'] == username:
            return redirect('/myprofile')
        user = db.read_babblers(username)
        babbles = db.read_user_babbles(username)
        followers = db.read_followers(username)
        subscriptions = db.read_subscriptions(username)
        followed = db.following(session['username'], username)
        nb_babbles = len(babbles)
        nb_followers = len(followers)
        nb_subscriptions = len(subscriptions)
        view = render_template('/partials/profile.html', user=user[0],
                               followed=followed, babbles=babbles, logged=True,
                               followers=followers, subscriptions=subscriptions,
                               nb_babbles=nb_babbles, nb_followers=nb_followers,
                               nb_subscriptions=nb_subscriptions)
        return view
    else:
        return redirect('/login')


@app.route('/tag/<tag>')
def tag_page(tag):
    if 'username' in session:
        babbles = db.read_babbles_with_tag(tag)
        view = render_template('/partials/tag_results.html', babbles=babbles, tag=tag, logged=True)
        return view
    else:
        return redirect('/login')


@app.route('/search')
def search_form():
    if 'username' in session:
        keyword = request.args.get('keyword')
        if keyword:
            babbles = db.read_babbles(keyword)
            babblers = db.read_babblers(keyword)
            babbles_with_tag = db.read_babbles_with_tag(keyword)
            babbles.extend(babbles_with_tag)
            return render_template('/partials/search_results.html',
                                   keyword=keyword, babbles=babbles,
                                   babblers=babblers, logged=True)
        else:
            username = session['username']
            babbles = db.get_babbles_from_followed_babblers(username)
            return render_template('index.html', babbler=username, babbles=babbles, logged=True)
    else:
        return redirect('/login')


# Validate if <username> is already taken.
@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    exists = False
    if db.validate_username(username):
        exists = True
    return str(exists)


if __name__ == '__main__':
    app.run()
