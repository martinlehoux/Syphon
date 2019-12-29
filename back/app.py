#! ./env/bin/python
from sys import argv
from time import time

import jwt
from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from kaga_logger import DEBUG, Logger
from peewee import DoesNotExist, IntegrityError
from werkzeug.exceptions import HTTPException

from conf import JWT_EXPIRES_IN, JWT_SECRET_KEY, PAGE_SIZE
from utils import token_protected
from validators import Record, User

APP = Flask(__name__)
CORS = CORS(APP)
APP.config['CORS_HEADERS'] = 'Content-Type'

LOGGER = Logger(DEBUG)

@APP.errorhandler(HTTPException)
def http_exception(err):
    return jsonify(error=str(err)), err.code

@APP.route('/token', methods=['POST'])
def token():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username:
        abort(400, "username is required")
    if not password:
        abort(400, "password is required")
    try:
        user = User.get(User.username == username)
        if user.password_hash is None:
            abort(403, f"User '{username} doesn't have a password set and can't log in")
        if not user.check_password(password):
            abort(400, f"Password is wrong for User '{username}'")
        jwt_token = jwt.encode(dict(exp=int(time()) + JWT_EXPIRES_IN, username=username), JWT_SECRET_KEY, algorithm='HS512')
        return jsonify(token=jwt_token.decode('utf-8')), 201
    except DoesNotExist:
        abort(404, f"User '{username}' not found")


@APP.route('/users', methods=['POST', 'GET'])
@token_protected
def user_list():
    if request.method == "GET":
        page = int(request.args.get('page') or 0)
        users = User.select().order_by(User.username).offset(page * PAGE_SIZE).limit(PAGE_SIZE)
        return jsonify([user.json() for user in users])
    if request.method == "POST":
        try:
            user = User.create(**request.json)
            return jsonify(user.json()), 201
        except (AssertionError, IntegrityError) as err:
            abort(400, err)

@APP.route('/users/<string:username>', methods=['GET'])
@token_protected
def user_detail(username: str):
    if request.method == 'GET':
        try:
            user = User.get(User.username == username)
            return jsonify(user.json())
        except DoesNotExist:
            abort(404, f"User '{username}' not found")

@APP.route('/users/<string:username>/records', methods=['GET', 'POST'])
@token_protected
def user_record_list(username: str):
    if request.method == 'GET':
        records = Record.select().where(Record.user == username)
        return jsonify([record.json() for record in records])
    if request.method == 'POST':
        try:
            record = Record.create(**request.json, user=username)
            record = Record.get_by_id(record.id)
            return jsonify(record.json()), 201
        except AssertionError as err:
            abort(400, err)

@APP.route('/records', methods=['GET'])
def record_list():
    if request.method == 'GET':
        records = Record.select()
        return jsonify([record.json() for record in records])

@APP.route('/records/<int:record_id>', methods=['DELETE'])
@token_protected
def record_detail(record_id: int):
    if request.method == 'DELETE':
        try:
            record = Record.get_by_id(record_id)
            record.delete_instance()
            return jsonify(), 204
        except DoesNotExist:
            abort(404, f"Record '{record_id}' not found'")

if __name__ == "__main__":
    try:
        HOSTNAME = argv[1]
    except IndexError:
        HOSTNAME = 'localhost'
    APP.run(debug=True, host=HOSTNAME)
