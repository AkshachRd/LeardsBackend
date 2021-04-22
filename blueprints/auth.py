import datetime

import jwt
from flask import Blueprint, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import exc
from models.user import User
from my_sqlalchemy import db
from services.auth import fetch_model, test
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

    return jsonify({'token': token.decode('utf-8')}), 200


@auth.route('/signup', methods=['POST'])
def signup():
    email = request.json['email']
    username = request.json['name']
    password = request.json['password']
    phone = request.json['phone']

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

    token = create_token(new_user.id)
    return jsonify({'token': token.decode('utf-8')}), 201


@auth.route('/logout')
def logout():
    return 'sing'#test()


@auth.route('/check_status')
def check_status(func):
    token = request.args.get('token')
    if not token:
        return jsonify({'massage': 'Missing token'}), 404

    data = jwt.decode(token, JWT_KEY)
    if data:
        return jsonify({'massage': 'Authorised', 'token': token}), 200
    else:
        return jsonify({'massage': 'Authorised', 'token': token}), 200


def create_token(userId):
    token = jwt.encode({
        'userId': userId,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
    }, JWT_KEY)

    return token
