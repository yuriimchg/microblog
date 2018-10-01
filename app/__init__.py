from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Create an instanсe of a flask application
app = Flask(__name__)
# Initialize Flask-Login instance
login = LoginManager(app)
# Create an instance of app configurations
app.config.from_object(Config)
# Create an instance of the database
db = SQLAlchemy(app)
# Create an instance of the database migration
migrate = Migrate(app,db)

# Import routes in the bottom of an app is OK, because
# importing routes in the top causes exceptions
from app import routes, models
