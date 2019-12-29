from __future__ import annotations

from datetime import datetime
from hashlib import scrypt
from os import environ

from peewee import (BlobField, CharField, DateField, ForeignKeyField,
                    IntegerField, Model, SqliteDatabase)

from conf import SCRYPT_SECRET_KEY

DB = SqliteDatabase(f"{environ.get('ENV')}.db")

class User(Model):
    class Meta:
        database = DB

    username = CharField(index=True, unique=True, primary_key=True)
    password_hash = BlobField(null=True)
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

    def update_password(self, password):
        self.password_hash = scrypt(bytes(password, 'utf-8'), salt=SCRYPT_SECRET_KEY, n=1<<14, r=8, p=1)
        self.save()

    def check_password(self, password):
        return scrypt(bytes(password, 'utf-8'), salt=SCRYPT_SECRET_KEY, n=1<<14, r=8, p=1) == self.password_hash


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
