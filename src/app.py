import os
import hashlib
import binascii
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
        'password': 'password'
    }
]
#  Hashing salt
salt = 'BabblerDefaultSalt'


@app.route('/')
def main():
    return render_template('index.html',
                           new_login=request.args.get('new_login'),
                           babbler=request.args.get('babbler'))


@app.route('/search')
def search_form():
    keyword = request.args.get('keyword')
    if keyword:
        return render_template('/partials/search_results.html', keyword=keyword)
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    view = render_template('partials/login.html',
                           newly_registered=request.args.get('newly_registered'),
                           invalid=request.args.get('invalid'))
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = hashlib.pbkdf2_hmac('sha256', data['password'].encode(), salt.encode(), 100000)
        password = str(binascii.hexlify(password))[2:-1]
        print('Received password: ', password)
        for user in users:
            if user['username'] == username:
                print('Found username')
                if user['password'] == password:
                    print('Found password')
                    view = redirect('/?new_login="True"&babbler=' + username)
    return view


@app.route('/register', methods=['GET', 'POST'])
def register():
    view = render_template('/partials/register.html')
    if request.method == 'POST':
        data = request.form
        password = hashlib.pbkdf2_hmac('sha256', data['password'].encode(), salt.encode(), 100000)
        password = str(binascii.hexlify(password))[2:-1]
        users.append({
            'username': data['username'],
            'public_name': data['public_name'],
            'password': password
        })
        print('Registered password: ', password)
        #  TODO: Add user to DB instead of locally

        return view
    else:
        return view


@app.route('/myprofile')
def my_profile():
    if session['logged_in']:
        return render_template('myprofile.html')
    else:
        return redirect(url_for('/login'))


@app.route('/babblers/<username>')
def babbler_profile(username):
    view = render_template('/partials/profile.html', user=username)
    return view


@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    exists = False
    for user in users:
        if user['username'] == username:
            exists = True
    return str(exists)


if __name__ == '__main__':
    app.run()
