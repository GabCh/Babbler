import shutil
import os
from src.babbler.babblerdb import BabblerDB
from random import randint
from flask import Flask
from pyfiglet import Figlet
import datetime

# Config data for DB
app = Flask(__name__)
app.config.from_object(__name__)
app.config['DB_HOST'] = 'localhost'
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = 'b4bbl3r1saw3s0m3'
app.config['DB_NAME'] = 'Babbler'

BABBLES_MAX = 2000
LINES_IN_FILES = 100

f = Figlet(font='slant')


def populate_users(db: BabblerDB):
    with open('../src/babbler/fake_user_data/users') as users:
        for user in users:
            user = user.replace('\n', '')
            username, public, password = user.split(', ', maxsplit=2)
            shutil.copy(os.path.abspath('../src/static/placeholders/profile.jpg'),
                        os.path.abspath('../src/static/images/' + str(username) + '.jpg'))
            db.add_babbler(username, public, password)
    users.close()


def populate_babbles(db: BabblerDB):
    with open('../src/babbler/fake_user_data/users') as users, open('../src/babbler/fake_user_data/tags') as tags:
        lines = users.readlines()
        tags_lines = tags.readlines()
        for i in range(6, BABBLES_MAX+5):
            message = f.renderText(tags_lines[randint(0, LINES_IN_FILES-1)].replace('\n', ''))
            tags = []
            for j in range(5):
                tags.append(tags_lines[randint(0, LINES_IN_FILES-1)].replace('\n', ''))
            username, _ = lines[randint(0, LINES_IN_FILES-1)].split(', ', maxsplit=1)
            time_s = datetime.datetime.now() - datetime.timedelta(days=randint(0, 5), seconds=randint(0, 60),
                                                                  minutes=randint(0, 60), weeks=randint(0, 4))
            db.add_babble(i, username, message, time_s, tags)
    users.close()


if __name__ == '__main__':
    db = BabblerDB(app)
    populate_users(db)
    populate_babbles(db)
