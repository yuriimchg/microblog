from flask import Flask

# Create an instanсe of a flask application
app = Flask(__name__)

# Import routes in the bottom of an app is OK, because
# importing routes in the top causes exceptions
from app import routes
