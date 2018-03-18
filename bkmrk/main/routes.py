from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from werkzeug.urls import url_parse

from bkmrk import db
from bkmrk.main.forms import EditProfileForm, SearchForm
from bkmrk.models import User, Book
from bkmrk.main import bp

from ..openlibrary.client import OpenLibraryClient


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
    results = {}
    if form.validate_on_submit():
        query = form.query.data
        return redirect(url_for('main.search', q=query))
    elif request.method == 'GET':
        q = request.args.get('q')
        if q is not None:
            client = OpenLibraryClient()
            results = client.search(q=q, limit=10)
    return render_template(
        'search.html',
        title='Search',
        form=form,
        results=results,
    )
