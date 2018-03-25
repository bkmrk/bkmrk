from datetime import datetime
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from bkmrk import db, login


# Association Tables

user_book = db.Table('user_book',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

book_publisher = db.Table('book_publisher',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('publisher_id', db.Integer, db.ForeignKey('publisher.id'), primary_key=True)
)

book_author = db.Table('book_author',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True),
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
    default_book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    books = db.relationship('Book', secondary=user_book)
    quotes = db.relationship('Quote', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except Exception:
            return None
        return User.query.get(id)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    subtitle = db.Column(db.String(128), nullable=True)
    quotes = db.relationship('Quote', backref='book')
    publishers = db.relationship('Publisher', secondary=book_publisher)
    authors = db.relationship('Author', secondary=book_author)
    identifier_id = db.Column(db.Integer, db.ForeignKey('identifier.id'))
    identifier = db.relationship('Identifier', backref=db.backref('book', uselist=False))
    ol_book_id = db.Column(db.Integer, db.ForeignKey('open_library_book.key'))
    ol_book = db.relationship('OpenLibraryBook', backref=db.backref('book', uselist=False))


class OpenLibraryBook(db.Model):
    key = db.Column(db.String(32), primary_key=True)
    url = db.Column(db.String(256))
    cover_s = db.Column(db.String(256))
    cover_m = db.Column(db.String(256))
    cover_l = db.Column(db.String(256))
    publish_date = db.Column(db.String(32))


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))


class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class Identifier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13))
    olid = db.Column(db.String(32), nullable=True)


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    quote = db.Column(db.Text)
    page = db.Column(db.Integer)
    comments = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
