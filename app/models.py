from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# inherited from db.Model - basic class for all Flask models
class User(db.Model):
    # Id column
    id = db.Column(db.Integer, primary_key = True)
    # Username column
    username = db.Column(db.String(64), index=True, unique=True)
    # E-mail column
    email = db.Column(db.String(128), index=True, unique=True)
    # Password column. Since the database can be compromised by thieves,
    #   it is better to store password_hash instead of passwords
    password_hash = db.Column(db.String(128))
    # Posts by user
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(640))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Post {self.body}'
