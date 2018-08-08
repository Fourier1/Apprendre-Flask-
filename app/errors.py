#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-

from flask import render_template
from . import app, db


@app.errorhandler(404)
def not_found_error(error):
    """
    Page d'erreur personnalisée 404
    :param error: 
    :return: 
    """
    web = '404.html'
    return render_template(web), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Page d'erreur personnalisée 500
    :param error: 
    :return: 
    """
    web = '500.html'
    db.session.rollback()
    return render_template(web), 500
