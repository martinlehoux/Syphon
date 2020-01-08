from datetime import date

from pytest import raises

from peewee import DoesNotExist, IntegrityError
from validators import Record, User


def teardown_function():
    User.delete().execute() # pylint: disable=no-value-for-parameter
    Record.delete().execute() # pylint: disable=no-value-for-parameter

def test_user_validator():
    with raises(AssertionError): # username = 1
        User.create(1, first_name="Martin", last_name="Lehoux", email="martin@lehoux.net", password="test1234")
    with raises(AssertionError): # username bad char
        User.create("°°°°°°°°", first_name="Martin", last_name="Lehoux", email="martin@lehoux.net", password="test1234")
    with raises(AssertionError): # username bad length
        User.create("abc", first_name="Martin", last_name="Lehoux", email="martin@lehoux.net", password="test1234")
    with raises(AssertionError): # email regex
        User.create("Kagamino", first_name="Martin", last_name="Lehoux", email="martinlehoux.net", password="test1234")
    with raises(AssertionError): # password to short
        User.create("Kagamino", first_name="Martin", last_name="Lehoux", email="martin@lehoux.net", password="a")
    user = User.create("Kagamino", first_name="Martin", last_name="Lehoux", email="martin@lehoux.net", password="test1234")
    assert user.password_hash == User.hash_password('test1234')
    with raises(IntegrityError): # username unique
        User.create("Kagamino", first_name="Martin", last_name="Lehoux", email="martin@lehoux.net", password="test1234")

def test_record_validator():
    user = User.create("Kagamino", first_name="Martin", last_name="Lehoux", email="martin@lehoux.net", password="test1234")
    with raises(AssertionError):
        Record.create(date=20191212, chrono=1000, user=user)
    Record.create(date=date.today(), chrono=1000, user=user)
    Record.create(date="2019-12-12", chrono=1000, user=user)
    with raises(AssertionError):
        Record.create(date=date.today(), chrono=1.1, user=user)
    with raises(AssertionError):
        Record.create(date=date.today(), chrono=1000, user=None)
    Record.create(date=date.today(), chrono=1000, user="Kagamino")
    with raises(DoesNotExist):
        Record.create(date=date.today(), chrono=1000, user="none")
