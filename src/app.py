import os
from flask import Flask, render_template, request
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'babbler.db'),
    SECRET_KEY='dev key (change later)',
    USERNAME='admin',
    PASSWORD='NodesBand420!'
))


@app.route("/")
def main():
    return "Bonjour et bienvenue!"


@app.route("/search")
def search_form():
    keyword = request.args.get('keyword')
    if keyword:
        return render_template('search_results.html', keyword=keyword)
    else:
        return render_template('search.html')


if __name__ == "__main__":
    app.run()
