from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin

from sqlalchemy import select, insert, text, exc
from src.models import user as user_table
from src.services.auth import create_token, check_status
import src.app as app

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def login():
    request_data_dict = request.get_json()
    email = request_data_dict['email']
    password = request_data_dict['password']

    stmt = (
        select([user_table]).
        where(user_table.c.email == email)
    )
    user = app.conn.execute(stmt).first()

    if not user.email:
        return jsonify({'message': 'User with this email does not exist'}), 404
    if not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid password'}), 403

    expires_in = 60 * 60 * 24  # 24 часа
    token = create_token(user.id_user, expires_in)
    response = make_response(jsonify({'userId': user.id_user, 'message': 'Successfully logged in!'}), 200)
    response.set_cookie('lrds', token, max_age=expires_in, httponly=True)

    return response


@auth_blueprint.route('/auth', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def login_token():
    token = request.cookies.get('lrds')

    if token:
        return check_status(token)
    else:
        return jsonify({'message': 'The users token was not provided'}), 400


@auth_blueprint.route('/signup', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def signup():
    request_data_dict = request.get_json()
    email = request_data_dict['email']
    username = request_data_dict['username']
    password = request_data_dict['password']

    stmt = (
        select([user_table]).
        where(user_table.c.email == email)
    )
    user = app.conn.execute(stmt).first()
    if user.username:
        return jsonify({'message': 'This email is already used'}), 409

    stmt = (
        insert(user_table).
        values(email=email, username=username, password_hash=generate_password_hash(password, method="sha256"))
    )
    try:
        new_user = app.conn.execute(stmt)
    except exc.SQLAlchemyError:
        return jsonify({'message': 'DB insert error'}), 500

    new_user_id = app.conn.execute(text('SELECT LAST_INSERT_ID()')).fetchone()[0]

    expires_in = 60 * 60 * 24  # 24 часа
    token = create_token(new_user_id, expires_in)
    response = make_response(jsonify({'message': 'Successfully signed up!'}), 201)
    response.set_cookie('lrds', token, max_age=expires_in, httponly=True)

    return response


@auth_blueprint.route('/logout', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def logout():
    response = make_response(jsonify({'message': 'Successfully loged out!'}), 200)
    response.set_cookie('lrds', '', max_age=0, httponly=True)

    return response
