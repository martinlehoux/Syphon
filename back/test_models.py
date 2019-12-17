from datetime import datetime, timedelta

from models import Record, User

def test_user():
    User.create(username="Kagamino")

def test_record():
    user = User(id=0, name="Kagamino")
    Record(id=0, date=datetime.now().date(), chrono=timedelta(seconds=6), user=user)
