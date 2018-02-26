from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from werkzeug.urls import url_parse

from bkmrk import db
from bkmrk.main.forms import EditProfileForm, BookForm
from bkmrk.models import User, Book
from bkmrk.main import bp


@bp.before_app_request
def before_request():
    pass


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = BookForm()
    if form.validate_on_submit():
        book = Book.query.filter_by(isbn13=form.isbn.data).first()
        if book is None:
            book = Book(isbn13=form.isbn.data)
            db.session.add(book)
            db.session.commit()
        # TODO: add book to user's books
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    books = current_user.books.paginate(page, current_app.config['BOOKS_PER_PAGE'], False)
    next_url = url_for('index', page=books.next_num) if books.has_next else None
    prev_url = url_for('index', page=books.prev_num) if books.has_prev else None
    return render_template(
        'index.html',
        title='Home',
        form=form,
        books=books.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    books = current_user.books.paginate(page, current_app.config['BOOKS_PER_PAGE'], False)
    next_url = url_for('user', page=books.next_num) if books.has_next else None
    prev_url = url_for('user', page=books.prev_num) if books.has_prev else None
    return render_template(
        'user.html',
        user=user,
        books=books.items,
        next_url=next_url,
        prev_url=prev_url,
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
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('you cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}'.format(username))
    return redirect(url_for('user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}'.format(username))
    return redirect(url_for('user', username=username))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    books = Book.paginate(page, current_app.config['BOOKS_PER_PAGE'], False)
    next_url = url_for('explore', page=books.next_num) if books.has_next else None
    prev_url = url_for('explore', page=books.prev_num) if books.has_prev else None
    return render_template(
        'index.html',
        title='Explore',
        books=books.items,
        next_url=next_url,
        prev_url=prev_url,
    )