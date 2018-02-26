from datetime import datetime, timedelta

import pytest

from .fixtures import *

from bkmrk.models import User, BookQuote


@pytest.fixture
def alice(db):
    user = User(username='alice', email='alice@example.com')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def bob(db):
    user = User(username='bob', email='bob@example.com')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def carol(db):
    user = User(username='carol', email='carol@example.com')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def dan(db):
    user = User(username='dan', email='dan@example.com')
    db.session.add(user)
    db.session.commit()
    return user


def test_password_hashing(db):
    """Test password hashing."""
    u = User(username='alice')
    u.set_password('cat')
    assert not u.check_password('dog')
    assert u.check_password('cat')


def test_follow_init(db, alice):
    """Test initial follow state."""
    assert len(alice.followed.all()) == 0
    assert len(alice.followers.all()) == 0


def test_follow(db, alice, bob):
    """Test follow user."""
    alice.follow(bob)
    db.session.commit()
    assert alice.is_following(bob)
    assert alice.followed.count() == 1
    assert alice.followed.first().username == 'bob'
    assert bob.followers.count() == 1
    assert bob.followers.first().username == 'alice'


def test_unfollow(db, alice, bob):
    """Test unfollow user."""
    alice.follow(bob)
    db.session.commit()
    alice.unfollow(bob)
    db.session.commit()
    assert not alice.is_following(bob)
    assert alice.followed.count() == 0
    assert bob.followers.count() == 0


def test_follow_book_quotes(db, alice, bob, carol, dan):
    now = datetime.utcnow()
    b1 = BookQuote(quote="quote from alice", user_id=alice.id, timestamp=now + timedelta(seconds=1))
    b2 = BookQuote(quote="quote from bob", user_id=bob.id, timestamp=now + timedelta(seconds=4))
    b3 = BookQuote(quote="quote from carol", user_id=carol.id, timestamp=now + timedelta(seconds=3))
    b4 = BookQuote(quote="quote from dan", user_id=dan.id, timestamp=now + timedelta(seconds=2))
    db.session.add_all([b1, b2, b3, b4])
    db.session.commit()

    alice.follow(bob)
    alice.follow(dan)
    bob.follow(carol)
    carol.follow(dan)
    db.session.commit()

    f1 = alice.followed_book_quotes().all()
    f2 = bob.followed_book_quotes().all()
    f3 = carol.followed_book_quotes().all()
    f4 = dan.followed_book_quotes().all()
    assert f1 == [b2, b4, b1]
    assert f2 == [b2, b3]
    assert f3 == [b3, b4]
    assert f4 == [b4]
