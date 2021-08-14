import datetime

from src import app
import jwt
from flask import jsonify, make_response


def create_token(user_id, expires_in):
    token = jwt.encode({
        'userId': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }, app.app.config['JWT_KEY'], algorithm="HS256")

    return token


def check_status(token):
    expires_in = 60 * 60 * 24  # 24 часа

    if not token:
        return jsonify({'message': 'Missing token'}), 404

    try:
        data = jwt.decode(token, app.app.config['JWT_KEY'], algorithms="HS256")

        token = create_token(data['UserId'], expires_in)
        response = make_response(jsonify({'userId': data['UserId'], 'message': 'Successfully logged in!'}), 200)
        response.set_cookie('lrds', token, max_age=expires_in, httponly=True)
        return response
    except jwt.exceptions.ExpiredSignatureError:
        return make_response('Invalid token', 401, {'WWW-Authenticate': 'Basic realm: "Access to the Leards"'})
