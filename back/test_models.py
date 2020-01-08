from datetime import datetime

from models import Record, User


def teardown_function():
    User.delete().execute() # pylint: disable=no-value-for-parameter
    Record.delete().execute() # pylint: disable=no-value-for-parameter


def test_user():
    User.create(username="Kagamino", first_name="Martin", last_name="Lehoux", email="martin@lehoux.net", password_hash=User.hash_password('test1234'))

def test_record():
    user = User(username="Kagamino")
    Record(date=datetime.now(), chrono=6000, user=user)
