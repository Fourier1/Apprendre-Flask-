#!/usr/bin/env python3
# -*- ncoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from .models import User


class LoginForm(FlaskForm):
    """
    FOrmulaire login 
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Connexion')


class RegistrationForm(FlaskForm):
    """
    enregistrer un utilisateur
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Paswword', validators=[DataRequired()])
    password2 = PasswordField('Repeat Paswword', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Enregistrer')

    def validate_username(self, username):
        """
        ne pas permetre deux meme mot de passe dans la BD
        :param username: 
        :return: 
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Utiliser un autre nom d\'utilisateur, celui-ci est déjà utiliser!")

    def validate_email(self, email):
        """
        ne pas permetre deux meme email dans la BD
        :param email: 
        :return: 
        """
        user = User.query.filter_by(username=email.data).first()
        if user is not None:
            raise ValidationError("Utiliser un autre eamil, celui-ci est déjà utiliser!")
