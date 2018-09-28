from flask import Flask
from config import Config

# Create an instanсe of a flask application
app = Flask(__name__)
app.config.from_object(Config)
# Import routes in the bottom of an app is OK, because
# importing routes in the top causes exceptions
from app import routes
