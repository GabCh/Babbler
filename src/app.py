import hashlib
import binascii

from flask import Flask, render_template, request, session, url_for, redirect
from data.babblerdb import BabblerDB


app = Flask(__name__)
app.config.from_object(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'minecraft371'
app.config['MYSQL_DATABASE_DB'] = 'Babbler'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


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

db = BabblerDB(app)
BABBLES_TABLE = 'babbles'
BABBLERS_TABLE = 'babblers'


@app.route('/')
def main():
    return render_template('index.html',
                           new_login=request.args.get('new_login'),
                           babbler=request.args.get('babbler'))


@app.route('/search')
def search_form():
    keyword = request.args.get('keyword')
    if keyword:
        babbles = db.read_table(BABBLES_TABLE, keyword, 'message')
        babblers = db.read_table(BABBLERS_TABLE, keyword, 'PublicName')
        return render_template('/partials/search_results.html', keyword=keyword, babbles=babbles, babblers=babblers)
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
        password = hashlib.pbkdf2_hmac('sha256', data['password'].encode(), salt.encode(), 65336)
        password = str(binascii.hexlify(password))[2:-1]
        print('Received password: ', password)
        for user in users:  # TODO: Search DB for user and pw
            if user['username'] == username:
                print('Found username')
                if user['password'] == password:
                    print('Found password')
                    return 'True'
    return view


@app.route('/register', methods=['GET', 'POST'])
def register():
    view = render_template('/partials/register.html')
    if request.method == 'POST':
        data = request.form
        password = hashlib.pbkdf2_hmac('sha256', data['password'].encode(), salt.encode(), 65336)
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
