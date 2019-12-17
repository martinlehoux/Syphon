from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List
from os import environ
import re
from peewee import (
    Model, SqliteDatabase,
    DateField, IntegerField, ForeignKeyField, CharField,
    DoesNotExist
)

db = SqliteDatabase(f"{environ.get('ENV')}.db")

class User(Model):
    class Meta:
        database = db

    username = CharField(index=True, unique=True, primary_key=True)
    first_name = CharField(index=True, null=True)
    last_name = CharField(index=True, null=True)

    def json(self):
        return dict(
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
        )

class Record(Model):
    class Meta:
        database = db

    date = DateField(index=True, default=datetime.now, formats=['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d'])
    chrono = IntegerField(index=True)
    user = ForeignKeyField(model=User, backref="records", on_delete='CASCADE')

    def json(self):
        return dict(
            id=self.id,
            date=self.date.isoformat(), # pylint: disable=no-member
            chrono=self.chrono,
            user=self.user.username
        )

db.connect()
db.create_tables([User, Record])