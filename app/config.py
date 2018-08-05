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
