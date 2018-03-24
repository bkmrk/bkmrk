from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length

from bkmrk.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class SearchForm(FlaskForm):
    isbn = StringField('ISBN', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_isbn(self, isbn):
        if len(isbn.data) != 10 and len(isbn.data) != 13:
            raise ValidationError("ISBN length should be either 10 or 13 digits.")


class AddBookForm(FlaskForm):
    submit = SubmitField('Add Book')


class RemoveBookForm(FlaskForm):
    submit = SubmitField('Remove Book')
