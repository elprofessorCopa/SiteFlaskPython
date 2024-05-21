from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# Initialisation de l'application Flask
app = Flask(__name__)

# Initialisation de Bcrypt pour le hachage des mots de passe
bcrypt = Bcrypt(app)

# Initialisation du gestionnaire de connexion
login_manager =  LoginManager()
login_manager.init_app(app)
login_manager.login_view ='connect'

# Configuration de l'application
app.config['SECRET_KEY'] = "dnqzRUHq1AJ_oPzrKcrNVg"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog2.db'

# Initialisation de SQLAlchemy et Migrate pour la base de données
db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin()
admin.init_app(app)

# Initialisation de Bootstrap4 pour le style de l'application
Bootstrap(app)

# Importation des routes de l'application
from app import routes
