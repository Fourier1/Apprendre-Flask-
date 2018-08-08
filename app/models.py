#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from . import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     )


class User(UserMixin, db.Model):
    """
    model User , table pour stocké les utilisateurs 
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(164), index=True, unique=True)
    password = db.Column(db.String(128))
    post = db.relationship('Post', backref='uthor', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )

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

    def avatar(self, size):
        """
        proprete de l'image
        :param size: int taille de l'image
        :return: 
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        """
        Ajouter un utilisateur (folloxer)
        :param user: 
        :return: 
        """
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """
        Suprimer un follower
        :param user: 
        :return: 
        """
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """
        Cette methode s'assure que l'action demander a un sens
        :param user: 
        :return: 
        """
        return self.followed.filter(
            followers.c.follower_id == user.id).count() > 0

    def followed_posts(self):
        """
        optenir les posts des utilisateur suivis 
        :return: 
        """
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


class Post(db.Model):
    """
    Stocké les posts de l'utilisateur
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140), index=True, unique=True)
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
