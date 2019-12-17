#! ./env/bin/python
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from kaga_logger import INFO, Logger, DEBUG
from validators import User, Record
from peewee import DoesNotExist
from sys import argv

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

logger = Logger(DEBUG)

@app.errorhandler(400)
def bad_request_handler(err):
    return jsonify(error=str(err)), 400

# @app.errorhandler(404)
# def page_not_found(err):
#     return jsonify(error=str(err)), 404

@app.route('/users', methods=['POST', 'GET'])
@cross_origin()
def user_list():
    if request.method == "GET":
        users = User.select()
        return jsonify([user.json() for user in users])
    elif request.method == "POST":
        try:
            user = User.create(**request.json)
            return jsonify(user.json()), 201
        except AssertionError as err:
            abort(400, err)

@app.route('/users/<string:username>', methods=['GET'])
@cross_origin()
def user_detail(username: str):
    if request.method == 'GET':
        try:
            user = User.get(User.username == username)
            return jsonify(user.json())
        except DoesNotExist:
            abort(404, f"user '{username}' not found")

@app.route('/users/<string:username>/records', methods=['GET', 'POST'])
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

@app.route('/records', methods=['GET'])
def record_list():
    if request.method == 'GET':
        records = Record.select()
        return jsonify([record.json() for record in records])

if __name__ == "__main__":
    try:
        hostname = argv[1]
    except IndexError:
        hostname = 'localhost'
    app.run(debug=True, host=hostname)
