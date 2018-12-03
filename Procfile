pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
mysql -u root -p < data/dump.sql
python data/populate.py
web: python src/app.py
