#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from flask import Flask

from .config import config

# BD
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)

# creation d'une extension de la bd
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import routes, models
