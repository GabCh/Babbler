import os
from data.babblerdb import BabblerDB
from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)
bd = BabblerDB(app)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'babbler.db'),
    SECRET_KEY='dev key (change later)',
    USERNAME='admin',
    PASSWORD='password'
))


@app.route("/")
def main():
    return "Bonjour et bienvenue!"


if __name__ == "__main__":
    app.run()
