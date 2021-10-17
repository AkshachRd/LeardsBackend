from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

from sqlalchemy import select, insert, text, exc
from src.models import user as user_table
from src.services.auth import create_token, get_user_id_from_token
import src.app as app_file

auth_blueprint = Blueprint('auth', __name__)

CORS(auth_blueprint, supports_credentials=True)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    request_data_dict = request.get_json()
    user_login = request_data_dict['login']
    password = request_data_dict['password']

    stmt = (
        select([user_table]).
        where(user_table.c.email == user_login)
    )
    user = app_file.conn.execute(stmt).first()

    if not user:
        return jsonify({'message': 'User with this email does not exist'}), 404
    if not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid password'}), 403

    token = create_token(user.id_user, app_file.app.config['EXPIRES_IN'])
    response = make_response(jsonify({'userId': user.id_user,
                                      'username': user.username,
                                      'email': user.email}), 200)
    response.set_cookie('lrds', token, app_file.app.config['EXPIRES_IN'], httponly=True, samesite="none", secure=True)

    return response


@auth_blueprint.route('/auth', methods=['POST'])
def login_token():
    token = request.cookies.get('lrds')
    if not token:
        return jsonify({'message': 'The users token was not provided'}), 400

    user_id = get_user_id_from_token(token)
    if not user_id:
        return make_response('Invalid token', 401, {'WWW-Authenticate': 'Basic realm: "Access to the Leards"'})

    stmt = (
        select([user_table]).
        where(user_table.c.id_user == user_id)
    )
    user = app_file.conn.execute(stmt).first()

    if not user:
        return jsonify({'message': 'User with this email does not exist'}), 404

    token = create_token(user_id, app_file.app.config['EXPIRES_IN'])
    response = make_response(jsonify({'userId': user_id,
                                      'username': user.username,
                                      'email': user.email}), 200)
    response.set_cookie('lrds',
                        token,
                        max_age=app_file.app.config['EXPIRES_IN'],
                        httponly=True,
                        samesite="none",
                        secure=True)
    return response


@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    request_data_dict = request.get_json()
    email = request_data_dict['email']
    username = request_data_dict['username']
    password = request_data_dict['password']

    stmt = (
        select([user_table]).
            where(user_table.c.email == email)
    )
    user = app_file.conn.execute(stmt).first()
    if user:
        return jsonify({'message': 'This email is already used'}), 409

    stmt = (
        insert(user_table).
            values(email=email, username=username, password_hash=generate_password_hash(password, method="sha256"))
    )
    try:
        new_user = app_file.conn.execute(stmt)
    except exc.SQLAlchemyError:
        return jsonify({'message': 'DB insert error'}), 500

    new_user_id = app_file.conn.execute(text('SELECT LAST_INSERT_ID()')).fetchone()[0]

    expires_in = 60 * 60 * 24  # 24 часа
    token = create_token(new_user_id, expires_in)
    response = make_response(jsonify({'userId': new_user_id}), 201)
    response.set_cookie('lrds', token, max_age=expires_in, httponly=True, samesite="none", secure=True)

    return response


@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Successfully loged out!'}), 200)
    response.set_cookie('lrds', '', max_age=0, httponly=True, samesite="none", secure=True)

    return response
