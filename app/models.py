from app import db

# inherited from db.Model - basic class for all Flask models
class User(db.Model):
    # Id column
    id = db.Column(db.Integer, primary_key = True)
    # Username column
    username = db.Column(db.String(64), index=True, unique=True)
    # E-mail column
    email = db.Column(db.String(120), index=True, unique=True)
    # Password column. Since the database can be compromised by thieves,
    #   it is better to store password_hash instead of passwords
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}'
