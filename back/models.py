from __future__ import annotations

from datetime import datetime
from os import environ

from peewee import (BlobField, CharField, DateField, ForeignKeyField, BooleanField,
                    IntegerField, Model, SqliteDatabase)

from utils import hash_password

ENV = environ.get('ENV')
DB = SqliteDatabase(f"{ENV}.db")

class User(Model):
    class Meta:
        database = DB

    username = CharField(index=True, unique=True, primary_key=True)
    email = CharField(index=True, unique=True, null=False)
    password_hash = BlobField(null=True)
    first_name = CharField(index=True, null=True)
    last_name = CharField(index=True, null=True)
    inscription_date = DateField(index=True, default=datetime.now, formats=['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d'])
    is_admin = BooleanField(default=False)
    is_member = BooleanField(default=False)

    @property
    def best_record(self):
        return self.records.select().order_by(Record.chrono).limit(1).get()

    def json(self):
        return dict(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            bestRecord=self.best_record.json(),
            inscriptionDate=self.inscription_date.iso_format(), # pylint: disable=no-member
            isAdmin=self.is_admin
        )

    def update_password(self, password):
        self.password_hash = hash_password(password)
        self.save()

    def check_password(self, password):
        return hash_password(password) == self.password_hash


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
