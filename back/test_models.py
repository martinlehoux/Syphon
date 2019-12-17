from datetime import datetime

from models import Record, User


def teardown_function():
    User.delete().execute() # pylint: disable=no-value-for-parameter
    Record.delete().execute() # pylint: disable=no-value-for-parameter

def test_user():
    User.create(username="Kagamino")

def test_record():
    user = User(username="Kagamino")
    Record(date=datetime.now(), chrono=6000, user=user)
