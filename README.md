# Babbler
Homemade twitter-like web application

# Liens

[Rapport](https://drive.google.com/open?id=1lx70liwcA8EB2HQazvDFgBolvkQ33gXP)

[Déploiement Heroku](https://babbler-deploy.herokuapp.com)

# Installation locale

Premièrement, modifiez le fichier `app.py` à la ligne 20 à 23. Insérez les informations de votre base de données MySQL locale.

Sur la racine du projet, exécutez les commandes suivantes en ordre.

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
mysql -u root -p < data/dump.sql
```

Par la suite, exécuter le fichier ```data/populate.py``` dans votre IDE. Celui-ci s'occupera d'ajouter des données au projet.

Finalement, il suffit de lancer l'application avec le fichier ```src/app.py```.

# Diagramme entité relation
![](doc/ERDiag.jpg) 
