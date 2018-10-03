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

    # Mail credentials to receive notifications about errors on the server
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    # Address of administrator
    ADMINS = ['']
