from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from bkmrk import db, login


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
    books = db.relationship('UserBook', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn13 = db.Column(db.Integer)

    def __repr__(self):
        return f'<Post {self.isbn13}>'


def UserBook(db.Model):
    '''Relational table for Users and Book.'''
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_book = db.Column(db.Integer, db.ForeignKey('book.id'))


class BookQuote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_book = db.Column(db.Integer, db.ForeignKey('book.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    quote = db.Column(db.Text)
    page_no = db.Column(db.Integer)
    comments = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
