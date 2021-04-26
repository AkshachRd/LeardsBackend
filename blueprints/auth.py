from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin

from sqlalchemy import exc
from models.user import User
from db import db
from services.auth import create_token, check_status

auth = Blueprint('auth', __name__)


@auth.route('/login_password', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def login_password():
    request_data_dict = request.get_json()
    email = request_data_dict['email']
    password = request_data_dict['password']

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'massage': 'User with this email does not exist'}), 404
    if not check_password_hash(user.password, password):
        return jsonify({'massage': 'Invalid password'}), 403

    token = create_token(user.id_user)

    return jsonify({'token': token, 'userId': user.id_user}), 200


@auth.route('/login_token', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def login_token():
    token = request.get_json()['token']

    return check_status(token)


@auth.route('/signup', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def signup():
    request_data_dict = request.get_json()
    email = request_data_dict['email']
    username = request_data_dict['username']
    password = request_data_dict['password']
    phone = request_data_dict['phone']

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'massage': 'This email is already used'}), 409

    new_user = User(email=email,
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

    token = create_token(new_user.id_user)
    return jsonify({'token': token}), 201


@auth.route('/logout', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def logout():
    token = request.get_json()['token']

    return check_status(token)
