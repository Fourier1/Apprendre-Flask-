#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from flask import render_template, flash, redirect, url_for

from . import app
from .froms import LoginForm


@app.route('/')
@app.route('/index')
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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {} , remember_me={}'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('index'))

    return render_template('login.html', title=title, form=form)


@app.route('/contact')
def contact():
    """
    page contact
    :return: 
    """
    title = "Contact"
    return render_template("contact.html", title=title)
