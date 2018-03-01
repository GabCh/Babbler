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


@app.route('/')
def main():
    return 'Bonjour et bienvenue!'


@app.route('/search')
def search_form():
    keyword = request.args.get('keyword')
    if keyword:
        return render_template('search_results.html', keyword=keyword)
    else:
        return render_template('search.html')


@app.route('/login')
def login():
    error = None
    if request.method == 'POST':
        if request.form['user'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('/home'))
    return render_template('login.html', error=error)


@app.route('/home')
def home():
    if session['logged_in']:
        return render_template('newsfeed.html')
    else:
        return render_template('homepage.html')


@app.route('/myprofile')
def profile():
    if session['logged_in']:
        return render_template('profile.html')
    else:
        return redirect(url_for('/login'))


if __name__ == '__main__':
    app.run()
