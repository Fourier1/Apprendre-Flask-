#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from flask import Flask

from .config import config

from flask_login import LoginManager

# BD
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

import os

app = Flask(__name__)
app.config.from_object(config)

# connexion de l'utilisateur
login = LoginManager(app)

# fonction d'affichage qui gere les connection
login.login_view = 'login'

# creation d'une extension de la bd
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if not app.debug:
    # configuration des parametre mail pour recevoir les erreurs par email
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # creation du fichier log et configuration
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from . import routes, models, errors
