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
    if not token:
        return jsonify({'message': 'Missing token'}), 404

    try:
        data = jwt.decode(token, app.app.config['JWT_KEY'], algorithms="HS256")

        return jsonify({'token': token, 'userId': data['UserId']}), 200
    except jwt.exceptions.ExpiredSignatureError:
        return make_response('Invalid token', 401, {'WWW-Authenticate': 'Basic realm: "Access to the Leards"'})
