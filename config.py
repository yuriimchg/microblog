import os
# absolute path to base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# config params are just class variables
class Config:
    # Password
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'guess_me_sucker'
    # URI to database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    # Turn off notifications on changes into the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
