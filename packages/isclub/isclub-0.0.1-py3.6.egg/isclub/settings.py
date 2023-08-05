import hashlib
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class BaseConfig():
    # DEBUG MODE
    DEBUG = False

    # SESSION KEY
    SECRET_KEY = hashlib.md5(os.urandom(12)).hexdigest()

    # SQLALCHEMY DATABASE
    #
    # In windows，Set "sqlite:////<Your database url>"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = "c61e251"
