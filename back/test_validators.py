from validators import User, Record
from pytest import raises
from peewee import DoesNotExist, IntegrityError
from datetime import date

def teardown_function():
    User.delete().execute() # pylint: disable=no-value-for-parameter
    Record.delete().execute() # pylint: disable=no-value-for-parameter

def test_user_validator():
    with raises(AssertionError):
        User.create(1)
    with raises(AssertionError):
        User.create("°")
    with raises(AssertionError):
        User.create("abc")
    User.create("abcd")
    with raises(IntegrityError):
        User.create("abcd")

def test_record_validator():
    user = User.create("abcd")
    with raises(AssertionError):
        Record.create(date=20191212, chrono=1000, user=user)
    Record.create(date=date.today(), chrono=1000, user=user)
    Record.create(date="2019-12-12", chrono=1000, user=user)
    with raises(AssertionError):
        Record.create(date=date.today(), chrono=1.1, user=user)
    with raises(AssertionError):
        Record.create(date=date.today(), chrono=1000, user=None)
    Record.create(date=date.today(), chrono=1000, user="abcd")
    with raises(DoesNotExist):
        Record.create(date=date.today(), chrono=1000, user="none")
    