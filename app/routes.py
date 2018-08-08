#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from . import app
from .froms import LoginForm, RegistrationForm, EditProfileFrom
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from .models import User
from . import db


# @before_request : enregistre la fonction décorée a éxécuter juste avant la fonction d'affichage
@app.before_request
def before_request():
    """
    Enregistrer les derniers heur de vicite pour un utilisateur
    :return: 
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


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
        },
        {
            'author': {'username': 'ONESYME'},
            'body': 'je suis onesyme le devéloppeur segnieur en python !'
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
    web = 'login.html'
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

    return render_template(web, title=title, form=form)


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
    web = "register.html"
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        users = User(username=form.username.data, email=form.email.data)
        users.set_password(form.password.data)
        db.session.add(users)
        db.session.commit()
        flash('Félicitaion l\'utilisateur a été enregistrer')
        return redirect(url_for('login'))
    return render_template(web, title=title, form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    """
    Definir la page de profilt de'utilisateur
    :return: 
    """
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test Post #1'},
        {'author': user, 'body': 'Test Post #2'},
        {'author': user, 'body': 'Test Post #3'},
        {'author': user, 'body': 'Test Post #4'},
    ]
    title = 'profile'
    web = 'users.html'
    return render_template(web, user=user, title=title, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    la vue de profile d'un utilisateur
    :return: 
    """
    title = 'Edité le Profile'
    web = "edit_profile.html"
    form = EditProfileFrom(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Vos changements ont été enregistrés')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template(web, title=title, form=form)
