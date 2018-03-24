from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from werkzeug.urls import url_parse

from bkmrk import db
from bkmrk import utils
from bkmrk.main.forms import EditProfileForm, SearchForm, AddBookForm, RemoveBookForm
from bkmrk.models import User, Book
from bkmrk.main import bp


@bp.before_app_request
def before_request():
    pass


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@bp.route('/home', methods=['GET'])
@login_required
def index():
    books = current_user.books
    books = [utils.get_openlibrary_book(book.isbn) for book in books]
    return render_template(
        'index.html',
        title='Home',
        books=books,
    )


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    books = current_user.books
    return render_template(
        'user.html',
        user=user,
        books=books,
    )


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        isbn = form.isbn.data
        return redirect(url_for('main.search', isbn=isbn))

    books = []
    if request.method == 'GET':
        isbn = request.args.get('isbn')
        if isbn:
            if len(isbn) == 10:
                isbn = '978{}'.format(isbn)
            ol_book = utils.get_openlibrary_book(isbn)
            if ol_book:
                book = Book.query.filter_by(isbn=isbn).first()
                if book is None:
                    book = Book(isbn=isbn)
                    db.session.add(book)
                    db.session.commit()
                ol_book['id'] = book.id
                books.append(ol_book)
    return render_template(
        'search.html',
        title='Search',
        form=form,
        books=books,
    )


@bp.route('/book/<id>', methods=['GET', 'POST'])
@login_required
def book(id):
    book = Book.query.filter_by(id=id).first_or_404()

    # figure out if the user has added this book
    if book in current_user.books:
        form = RemoveBookForm()
    else:
        form = AddBookForm()

    if form.validate_on_submit():
        if book in current_user.books:
            current_user.books.remove(book)
            db.session.commit()
        else:
            current_user.books.append(book)
            db.session.commit()
        return redirect(url_for('main.book', id=book.id))

    ol_book = utils.get_openlibrary_book(book.isbn)
    return render_template(
        'book.html',
        title=ol_book.get('title'),
        form=form,
        book=ol_book,
    )
