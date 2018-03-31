# Babbler
Homemade twitter-like web application

# Installation
```bash
sudo pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Pour PyCharm, il faut effectuer cette étape:
![](doc/mark_as_source.png?raw=true) 

- Pour la BD, il faut configurer le sql_mode ainsi:
```bash
STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```
![](doc/sql_mode.png?raw=true) 

# Diagramme entité relation
![](doc/ERDiag.png?raw=true) 
