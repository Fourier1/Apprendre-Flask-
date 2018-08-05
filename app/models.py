#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from . import db
from datetime import datetime


class User(db.Model):
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
