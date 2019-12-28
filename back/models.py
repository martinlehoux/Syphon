from __future__ import annotations

from datetime import datetime
from os import environ

from peewee import (CharField, DateField, ForeignKeyField, IntegerField, Model,
                    SqliteDatabase)

DB = SqliteDatabase(f"{environ.get('ENV')}.db")

class User(Model):
    class Meta:
        database = DB

    username = CharField(index=True, unique=True, primary_key=True)
    first_name = CharField(index=True, null=True)
    last_name = CharField(index=True, null=True)

    @property
    def best_record(self):
        return self.records.select().order_by(Record.chrono).limit(1).get()

    def json(self):
        return dict(
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            bestRecord=self.best_record.json()
        )

class Record(Model):
    class Meta:
        database = DB

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

DB.connect()
DB.create_tables([User, Record])
