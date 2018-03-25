from openlibrary_api.client import OpenLibraryClient

from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from werkzeug.urls import url_parse

from bkmrk import db
from bkmrk.main.forms import EditProfileForm, SearchForm, AddQuoteForm
from bkmrk.models import User, Book, Quote, Author, OpenLibraryBook, Publisher, Identifier
from bkmrk.main import bp


def get_openlibrary_book(isbn, client=None):
    if client is None:
        client = OpenLibraryClient()
    bibkey = 'ISBN:{}'.format(isbn)
    ol_book = client.books(bibkeys=bibkey, format='json', jscmd='data')
    return ol_book.get(bibkey)


@bp.before_app_request
def before_request():
    pass


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@bp.route('/home', methods=['GET'])
@login_required
def index():
    books = current_user.books
    return render_template(
        'index.html',
        title='Home',
        books=books,
    )


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template(
        'user.html',
        user=user,
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


def add_openlibrary_book_to_databases(ol_book_json):
    publishers = []
    ol_publishers = ol_book_json.get('publishers')
    for publisher in ol_publishers:
        name = publisher.get('name')
        p = Publisher.query.filter_by(name=name).first()
        if p is None:
            p = Publisher(name=name)
            db.session.add(p)
        publishers.append(p)
    db.session.commit()

    authors = []
    ol_authors = ol_book_json.get('authors')
    for author in ol_authors:
        name = author.get('name')
        a = Author.query.filter_by(name=name).first()
        if a is None:
            a = Author(name=name)
            db.session.add(a)
        authors.append(a)
    db.session.commit()

    # TODO: Verify if I can always grab the first element
    isbn = ol_book_json.get('identifiers').get('isbn_13')[0]
    olid = ol_book_json.get('identifiers').get('openlibrary')[0]
    identifier = Identifier.query.filter_by(isbn=isbn).first()
    if identifier is None:
        identifier = Identifier(isbn=isbn, olid=olid)
        db.session.add(identifier)
    db.session.commit()

    key = ol_book_json.get('key')
    ol_book = OpenLibraryBook.query.filter_by(key=key).first()
    if ol_book is None:
        ol_book = OpenLibraryBook(
            key=key,
            url=ol_book_json.get('url'),
            cover_s=ol_book_json.get('cover').get('small'),
            cover_m=ol_book_json.get('cover').get('medium'),
            cover_l=ol_book_json.get('cover').get('large'),
            publish_date=ol_book_json.get('publish_date'),
        )
        db.session.add(ol_book)
    db.session.commit()

    book = identifier.book
    if book is None:
        book = Book(
            title=ol_book_json.get('title'),
            subtitle=ol_book_json.get('subtitle'),
            publishers=publishers, authors=authors,
            identifier=identifier,
            ol_book=ol_book,
        )
        db.session.add(book)
    db.session.commit()


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
            ol_book = get_openlibrary_book(isbn)
            if ol_book:
                add_openlibrary_book_to_databases(ol_book)
                identifier = Identifier.query.filter_by(isbn=isbn).first()
                book = identifier.book
                books.append(book)
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

    # Get the quotes that belong to this user and to this book
    book_quotes = book.quotes
    user_quotes = current_user.quotes
    quotes = list(set(book_quotes).intersection(set(user_quotes)))
    quotes = sorted(quotes, key=lambda quote: quote.page)

    return render_template(
        'book.html',
        title=book.title,
        book=book,
        quotes=quotes,
    )


@bp.route('/book/<id>/add')
@login_required
def add_book(id):
    book = Book.query.filter_by(id=id).first_or_404()

    if book not in current_user.books:
        current_user.books.append(book)
        db.session.commit()
    return redirect(url_for('main.book', id=book.id))


@bp.route('/quote', methods=['GET', 'POST'])
@login_required
def quote():
    book_id = request.args.get('book_id')
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        flash('book_id={} does not exist'.format(book_id))
        return render_template(
            'quote.html',
            title='',
        )

    form = AddQuoteForm()

    if form.validate_on_submit():
        quote = Quote(
            user_id=current_user.id,
            book_id=book_id,
            quote=form.quote.data,
            page=form.page.data,
            comments=form.comments.data)
        db.session.add(quote)
        db.session.commit()
        return redirect(url_for('main.book', id=book_id))

    return render_template(
        'quote.html',
        title=book.title,
        form=form,
    )
