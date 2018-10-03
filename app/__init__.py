from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# Use logging package to write logs
import logging
# Send email notifications about errors with SMTPHandler
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

# Create an instanсe of a flask application
app = Flask(__name__)

# Initialize Flask-Login instance
login = LoginManager(app)
# Define endpoint to log in into system
login.login_view = 'login'

# Create an instance of app configurations
app.config.from_object(Config)

# Create an instance of the database
db = SQLAlchemy(app)

# Create an instance of the database migration
migrate = Migrate(app,db)

# In case of disabled debug mode
if not app.debug:
    # SEND INFORMATION ABOUT ERRORS TO EMAIL
    # This won't work if there is no mail_server
    if app.config['MAIL_SERVER']:
        auth = None
        # Check if mail is assigned
        if app.config['MAIL_USERNAME'] and app.config["MAIL_PASSWORD"]:
            auth = (app.config['MAIL_USERNAME'], app.config["MAIL_PASSWORD"])
        # Options for enabling / disabling TLS
        secure = None
        if app.config["MAIL_USE_TLS"]:
            secure = ()
        # Define an instance of SMTPHandler
        mail_handler = SMTPHandler(
                mailhost = (app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                fromaddr = 'no_reply@' + app.config["MAIL_SERVER"],
                toaddrs = app.config['ADMINS'], subject = 'Your microblog server is down',
                credentials = auth, secure = secure
            )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # If there is no log directory, create it
    if not os.path.exists('logs'):
        os.mkdir('logs')
    # rotate the log, ensuring that its size is less than 10Kb and count <= 10
    file_handler = RotatingFileHandler('logs/microblog.log',
                                        maxBytes=10240,
                                        backupCount=10)

    # Provide string formatting for the single log
    file_handler.setFormatter(logging.Formatter(
    '%(actime)s  %(levelname)s:  %(message)s [in %(pathname)s:%(lineno)d]'))
    # Set level of the logging to INFO
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    # Set level of the logging to INFO
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
# Import routes in the bottom of an app is OK, because
# importing routes in the top causes exceptions
from app import routes, models, errors
