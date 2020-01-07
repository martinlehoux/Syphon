from __future__ import annotations

from datetime import datetime
from os import environ
from time import time
from hashlib import scrypt

from peewee import (BlobField, CharField, DateField, ForeignKeyField, BooleanField,
                    IntegerField, Model, SqliteDatabase, DoesNotExist)
import jwt

from conf import SCRYPT_SECRET_KEY, JWT_EXPIRES_IN, JWT_SECRET_KEY

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
        try:
            return self.records.select().order_by(Record.chrono).limit(1).get()
        except DoesNotExist:
            return None

    def json(self):
        return dict(
            username=self.username,
            email=self.email,
            firstName=self.first_name,
            lastName=self.last_name,
            bestRecord=self.best_record.json() if self.best_record else self.best_record,
            inscriptionDate=self.inscription_date.isoformat(), # pylint: disable=no-member
            isAdmin=self.is_admin,
            isMember=self.is_member,
            hasPassword=bool(self.password_hash)
        )

    @staticmethod
    def hash_password(password: str) -> bytes:
        return scrypt(bytes(password, 'utf-8'), salt=SCRYPT_SECRET_KEY, n=1<<14, r=8, p=1)

    def create_token(self) -> str:
        return jwt.encode(
            dict(
                exp=int(time()) + JWT_EXPIRES_IN,
                username=self.username,
                isAdmin=self.is_admin,
                isMember=self.is_member
            ),
            JWT_SECRET_KEY,
            algorithm='HS512'
        ).decode('utf-8')

    def update_password(self, password):
        self.password_hash = User.hash_password(password)
        self.save()

    def check_password(self, password) -> bool:
        return User.hash_password(password) == self.password_hash


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
