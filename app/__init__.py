#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from flask import Flask

from .config import config

app = Flask(__name__)
app.config.from_object(config)

from . import routes
