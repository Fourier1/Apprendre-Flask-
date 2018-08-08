#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os

basadir = os.path.abspath(os.path.dirname(__file__))


# ficher de configuration
class config(object):
    """
    fochier de configuaration du projet
    """
    SECRET_KEY = os.environ.get('SECRET_KET') or 'LA_CLET_PRIVEE'

    # configuration de la base de donnée
    # spécifier le chemin de la base de donnée (app.db)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basadir, 'app.db')
    # desactivver l'option qui signale a l'appliction chaque fois qu'une modifications est sur le point d'etre effectuée
    #  dans la base de donnée
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ajouter les detail du serveur de mail pour reçevoir les erreurs pas mail export Variable | windows use set
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
