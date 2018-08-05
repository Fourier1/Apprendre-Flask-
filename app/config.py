#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os


# ficher de configuration
class config(object):
    """
    fochier de configuaration du projet
    """
    SECRET_KEY = os.environ.get('SECRET_KET') or 'LA_CLET_PRIVE'
