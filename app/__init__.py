#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from flask import Flask

from .config import config

from flask_login import LoginManager

# BD
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)

# connexion de l'utilisateur
login = LoginManager(app)

# fonction d'affichage qui gere les connection
login.login_view = 'login'

# creation d'une extension de la bd
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import routes, models
