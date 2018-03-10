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


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/search')
def search_form():
    keyword = request.args.get('keyword')
    if keyword:
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

@app.route('/myfeed')
def feed():
    posts = [
        {
            "user": "Jannik",
            "time": "16h50",
            "message": "Salut tout le monde! :)"
        },
        {
            "user": "Choupi",
            "time": "16h25",
            "message": "Pour vrai tyl"
        },
        {
            "user": "Gabriel",
            "time": "16h21",
            "message": "420 Blaze it !!!!!"
        }
    ]
    return render_template('partials/feed.html', cards=posts)


if __name__ == '__main__':
    app.run()
