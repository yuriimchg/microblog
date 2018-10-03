from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
# login components: get_id, is_auth, is_active, is_anon
from flask_login import UserMixin
# generate avatar
from hashlib import md5

# Load user
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

followers = db.Table('followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

# inherited from db.Model - basic class for all Flask models
class User(UserMixin, db.Model):
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
    # Information about user
    about_me = db.Column(db.String(640))
    # Timestamp, when the user last seen
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
    'User', secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        #
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def follow(self, user):
        # Follow the user
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        # Unfollow the user
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        # Return count of friends
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    def followed_posts(self):
        # Choose only followed posts from the database
        followed = Post.query.join(followers,
        (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        # Choose own posts from the database
        own = Post.query.filter_by(user_id=self.id)
        # Unite own and followed posts
        return followed.union(own).order_by(Post.timestamp.desc())
    

    def __repr__(self):
        return f'<User {self.username}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(640))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Post {self.body}'
