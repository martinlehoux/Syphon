import re
from datetime import date as datetype
from typing import List, Union

from models import Record as RecordModel
from models import User as UserModel
from utils import hash_password


class User(UserModel):
    @staticmethod
    def create(username: str, first_name: str, last_name: str, email: str, password: str): # pylint: disable=arguments-differ
        # username
        assert isinstance(username, str), "User.username must be a str."
        assert re.match(r'^[\w.-]+$', username), "User.username must use only a-zA-Z, _, - or . characters."
        assert len(username) >= 4, "User.username must length 4 characters or more."
        # first_name
        assert isinstance(first_name, str), "User.first_name must be a str."
        assert len(first_name) > 0, "User.first_name must length more than 0 characters."
        # last_name
        assert isinstance(last_name, str), "User.last_name must be a str."
        assert len(last_name) > 0, "User.last_name must length more than 0 characters."
        # password
        assert isinstance(password, str)
        assert len(password) >= 4, "User.password must length 4 characters or more."
        password_hash = hash_password(password)
        # email
        assert isinstance(email, str)
        assert re.match(r'^[\w.%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email), "User.email must be an email str. (%s)" % email

        return UserModel.create(username=username, first_name=first_name, last_name=last_name, password_hash=password_hash, email=email)


class Record(RecordModel):
    @staticmethod
    def create(date: Union[str, datetype], chrono: int, user: Union[str, UserModel]): # pylint: disable=arguments-differ
        # date
        assert isinstance(date, (str, datetype)), "Record.date must be a str or a date."
        # chrono
        assert isinstance(chrono, int), "Record.chrono must be an int."
        assert chrono > 0, "Record.chrono must be greater than 0."
        # user
        assert user is not None, "Record.user can't be None"
        assert isinstance(user, (str, UserModel)), "Record.user must be a str or a User."
        if isinstance(user, str):
            UserModel.get_by_id(user)

        return RecordModel.create(date=date, chrono=chrono, user=user)
