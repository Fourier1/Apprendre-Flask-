#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request

from . import app
from .froms import LoginForm, RegistrationForm

from flask_login import current_user, login_user, logout_user, login_required

from .models import User
from . import db


@app.route('/')
@app.route('/index')
# @login_required : demande une authentification pour voir cette page
def index():
    """
    index page
    :return: 
    """
    user = {'username': 'SAINT FOURIER'}
    posts = [
        {
            'author': {'username': 'SAINT'},
            'body': 'je suis le plus fort de la planete Terre!'
        },
        {
            'author': {'username': 'FOURIER'},
            'body': 'le monde n\'est rien d\'autre que du materiel!'
        }
    ]
    title = "Home"
    web = 'index.html'
    return render_template(web, title=title, user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Form login
    :return: 
    """
    title = "Sign In"
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nom d\'utilisateur ou mot de passe inccorect')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_for(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template("login.html", title=title, form=form)


@app.route('/contact')
def contact():
    """
    page contact
    :return: 
    """
    title = "Contact"
    return render_template("contact.html", title=title)


@app.route('/logout')
def logout():
    """
    déconnexion des utilisateurs
    :return: 
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=["GET", "POST"])
def register():
    """
    Enregistrer un utilisateur
    :return: 
    """
    title = "Enregistrement"
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Félicitaion l\'utilisateur a été enregistrer')
        return redirect(url_for('login'))
    return render_template("register.html", title=title, form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    """
    Definir la page de profilt de'utilisateur
    :return: 
    """
    user = User.query.filter_by(username=username).first_or_404()
    port = [
        {'auteur ': user, 'Text ': 'Test Post #1'},
        {'auteur ': user, 'Text ': 'Test Post #2'}
    ]
    return render_template('users.html', user=user, post=port)
