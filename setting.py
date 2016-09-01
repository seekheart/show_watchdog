import os
class Config:
    DEBUG = False
    TESTING = False
    PORT = 3000
    USER = os.environ.get('USER', None)
    PW = os.environ.get('PW', None)
    DBNAME = os.environ.get('DBNAME', None)

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@localhost/{}'.format(USER, PW, DBNAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(Config):
    DEBUG = True