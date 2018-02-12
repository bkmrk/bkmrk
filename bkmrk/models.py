from datetime import datetime
from bkmrk import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    book_quotes = db.relationship('BookQuote', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn13 = db.Column(db.Integer)

    def __repr__(self):
        return f'<Post {self.isbn13}>'


class BookQuote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_book = db.Column(db.Integer, db.ForeignKey('book.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    quote = db.Column(db.Text)
    page_no = db.Column(db.Integer)
    comments = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
