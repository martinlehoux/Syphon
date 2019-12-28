#! ./env/bin/python
from sys import argv

from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin
from kaga_logger import DEBUG, Logger
from peewee import DoesNotExist, IntegrityError

from validators import Record, User

APP = Flask(__name__)
CORS = CORS(APP)
APP.config['CORS_HEADERS'] = 'Content-Type'

LOGGER = Logger(DEBUG)
PAGE_SIZE = 10


@APP.errorhandler(400)
def bad_request(err):
    return jsonify(error=str(err)), 400

@APP.errorhandler(404)
def page_not_found(err):
    return jsonify(error=str(err)), 404

@APP.route('/users', methods=['POST', 'GET'])
@cross_origin()
def user_list():
    if request.method == "GET":
        page = int(request.args.get('page')) or 0
        users = User.select().order_by(User.username).offset(page * PAGE_SIZE).limit(PAGE_SIZE)
        return jsonify([user.json() for user in users])
    if request.method == "POST":
        try:
            user = User.create(**request.json)
            return jsonify(user.json()), 201
        except (AssertionError, IntegrityError) as err:
            abort(400, err)

@APP.route('/users/<string:username>', methods=['GET'])
@cross_origin()
def user_detail(username: str):
    if request.method == 'GET':
        try:
            user = User.get(User.username == username)
            return jsonify(user.json())
        except DoesNotExist:
            abort(404, f"User '{username}' not found")

@APP.route('/users/<string:username>/records', methods=['GET', 'POST'])
@cross_origin()
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
