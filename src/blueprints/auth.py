from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin

from sqlalchemy import exc
from src.models.user import User
from src import db
from src.services.auth import create_token, check_status

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def login():
    request_data_dict = request.get_json()
    email = request_data_dict['email']
    password = request_data_dict['password']

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User with this email does not exist'}), 404
    if not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid password'}), 403

    expires_in = 60 * 60 * 24  # 24 часа
    token = create_token(user.id_user, expires_in)
    response = make_response(jsonify({'userId': user.id_user, 'message': 'Successfully logged in!'}), 200)
    response.set_cookie('lrds', token, max_age=expires_in, httponly=True)

    return response


@auth.route('/login_token', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def login_token():
    token = request.cookies.get('lrds')

    if token:
        return check_status(token)
    else:
        return jsonify({'message': 'The user\'s token was not provided'}), 400


@auth.route('/signup', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def signup():
    request_data_dict = request.get_json()
    email = request_data_dict['email']
    username = request_data_dict['username']
    password = request_data_dict['password']

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'message': 'This email is already used'}), 409

    new_user = User(email=email,
                    username=username,
                    password_hash=generate_password_hash(password, method='sha256'),
                    )
    try:
        db.db.session.add(new_user)
        db.db.session.commit()
    except exc.SQLAlchemyError:
        db.db.session.rollback()
        return jsonify({'message': 'DB insert error'}), 500

    expires_in = 60 * 60 * 24  # 24 часа
    token = create_token(new_user.id_user, expires_in)
    response = make_response(jsonify({'message': 'Successfully signed up!'}), 201)
    response.set_cookie('lrds', token, max_age=expires_in, httponly=True)

    return response


@auth.route('/logout', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def logout():
    response = make_response(jsonify({'message': 'Successfully loged out!'}), 200)
    response.set_cookie('lrds', '', max_age=0, httponly=True)

    return response
