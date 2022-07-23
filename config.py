import os
from os import getenv


def get_config_file() ->dict:
    conf= dict()

    db_name = getenv('DB_NAME')
    db_user = getenv('DB_USER')
    db_pass = getenv('DB_PASSWD')
    db_host = getenv('DB_HOST')
    db_port = getenv('DB_PORT')
    db_credentials = f'{db_user}:{db_pass}'
    db_socket = f'{db_host}:{db_port}'
    conf["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{db_credentials}@{db_socket}/{db_name}'

    conf["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    SECRET_KEY = os.urandom(32)
    #app.config['SECRET_KEY'] = SECRET_KEY
    conf['SECRET_KEY'] = getenv('APP_KEY')
   
    #conf["SECRET_KEY"] = SECRET_KEY
    return conf
    




# SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# or app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect to the database


# TODO IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI = 'postgresql://nshimiyimana:Imbata_2@localhost:5432/fyyur'
