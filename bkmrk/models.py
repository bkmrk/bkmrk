from datetime import datetime
from time import time

import jwt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from bkmrk import app, db, login


# Association Tables

user_book = db.Table('user_book',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    about_me = db.Column(db.String(140))

    book_quotes = db.relationship('BookQuote', backref='user', lazy='dynamic')
    books = db.relationship('user_book', backref='user', lazy='dynamic')

    books = db.relationship(
        'Book', secondary=user_book,
        primaryjoin=(user_book.c.user_id == id),
        # secondaryjoin=() ???
        backref=db.backref('user_book', lazy='dynamic'), lazy='dynamic')

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_book_quotes(self):
        """Return book quotes from followed users in most recent order"""
        followed = BookQuote.query.join(
            followers, (followers.c.followed_id == BookQuote.user_id)).filter(
                followers.c.follower_id == self.id)
        own = BookQuote.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(BookQuote.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return User.query.get(id)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn13 = db.Column(db.Integer)

    def __repr__(self):
        return '<Post {}>'.format(self.isbn13)


class BookQuote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quote = db.Column(db.Text)
    page_no = db.Column(db.Integer)
    comments = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
