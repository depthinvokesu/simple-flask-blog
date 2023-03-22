from os import environ, path
from dotenv import load_dotenv

# return an absolute path of a of current file folder
script_dir = path.abspath(path.dirname(__file__))

# return a parent folder
#parent_dir = path.split(script_dir)[0]

# appends '.env' part to a parent directory since the file is there and loads it
load_dotenv(path.join(script_dir, '.env'))

class Config(object):
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SECRET_KEY = environ.get('SECRET_KEY')

class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_SQLALCHEMY_DATABASE_URI')
    FLASK_ENV = 'production'

class DevConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_SQLALCHEMY_DATABASE_URI')
    FLASK_ENV = 'development'
