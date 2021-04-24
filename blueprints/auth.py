import datetime

import jwt
from flask import Blueprint, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin

from sqlalchemy import exc
from models.user import User
from my_sqlalchemy import db
from settings import JWT_KEY

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'massage': 'User with this email does not exist'}), 404
    if not check_password_hash(user.password, password):
        return jsonify({'massage': 'Invalid password'}), 403

    token = create_token(user.id_user)

    return jsonify({'token': token}), 200


@auth.route('/signup', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def signup():
    # TODO: лучше бы оттестировать это всё на лакальной БД
    request_data_dict = request.get_json()
    user_id = request_data_dict['userId']
    email = request_data_dict['email']
    username = request_data_dict['username']
    password = request_data_dict['password']
    phone = request_data_dict['phone']

    user = User.query.filter_by(id_user=user_id).first()
    if user:
        return jsonify({'massage': 'This ID is already used'}), 409
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'massage': 'This email is already used'}), 409

    new_user = User(id_user=user_id,
                    email=email,
                    username=username,
                    password_hash=generate_password_hash(password, method='sha256'),
                    phone=phone
                    )
    try:
        db.session.add(new_user)
        db.session.commit()
    except exc.SQLAlchemyError:
        db.session.rollback()
        return jsonify({'massage': 'DB insert error'}), 500

    token = create_token(user_id)
    return jsonify({'token': token}), 201


@auth.route('/logout', methods=['POST'])
def logout():
    password = request.form.get('password')
    return password


@auth.route('/check_status', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type'])
def check_status():
    token = request.get_json()['token']
    if not token:
        return jsonify({'massage': 'Missing token'}), 404

    try:
        data = jwt.decode(token, JWT_KEY, algorithms="HS256")

        return jsonify({'massage': 'Authorised', 'token': token, 'data': data}), 200
    except jwt.exceptions.ExpiredSignatureError:
        return jsonify({'massage': 'Unauthorised', 'token': token}), 200


def create_token(user_id):
    token = jwt.encode({
        'userId': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
    }, JWT_KEY, algorithm="HS256")

    return token
