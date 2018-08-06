#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from . import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    model User , table pour stocké les utilisateurs 
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(164), index=True, unique=True)
    password = db.Column(db.String(128))
    post = db.relationship('Post', backref='uthor', lazy='dynamic')

    def __repr__(self):
        """
        champ a retouner pour afficher
        :return: 
        """
        return '< User {} >'.format(self.username), '< email {} >'.format(self.email)

    def set_password(self, password):
        """
        Hashage du mot de passe 
        :param password: string mot de passe
        :return: 
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        verification du mot de passe hasher  
        :param password: string mot de passe
        :return: 
        """
        return check_password_hash(self.password, password)


class Post(db.Model):
    """
    Stocké les posts de l'utilisateur
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """
        champ a retouner pour afficher
        :return: 
        """
        return '< Post {} >'.format(self.body), '< Times {} >'.format(self.timestamp)


# gerder les donnée de l'utilisateur connecter en session via son ID
@login.user_loader
def load_user(id):
    """
    sotcké les données de l'utilisateur en session
    :param id: 
    :return: 
    """
    return User.query.get(int(id))
