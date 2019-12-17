import re
from datetime import date as datetype
from typing import Union

from models import Record as RecordModel
from models import User as UserModel


class User(UserModel):
    @staticmethod
    def create(username: str, first_name: str = None, last_name: str = None): # pylint: disable=arguments-differ
        # username
        assert isinstance(username, str), "User.username must be a str."
        assert re.match(r'^[\w.-]+$', username), "User.username must use only a-zA-Z, _, - or . characters."
        assert len(username) >= 4, "User.username must length 4 characters or more."
        # first_name
        # last_name

        return UserModel.create(username=username, first_name=first_name, last_name=last_name)


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
        assert isinstance(user, (str, UserModel))
        if isinstance(user, str):
            UserModel.get_by_id(user)

        return RecordModel.create(date=date, chrono=chrono, user=user)
