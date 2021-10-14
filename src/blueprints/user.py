from flask import Blueprint, request, jsonify, make_response
from flask_cors import CORS
from src.services.auth import get_user_id_from_token

from src.services.user import fetch_user_model

user_blueprint = Blueprint('user_blueprint', __name__)

CORS(user_blueprint, supports_credentials=True)


@user_blueprint.route('/fetch_user_data', methods=['POST'])
def fetch_model():
    token = request.cookies.get('lrds')
    if not token:
        return jsonify({'message': 'The users token was not provided'}), 400

    user_id = get_user_id_from_token(token)
    if not user_id:
        return make_response('Invalid token', 401, {'WWW-Authenticate': 'Basic realm: "Access to the Leards"'})

    model = fetch_user_model(user_id)
    return jsonify({'userData': model}), 200


@user_blueprint.route('/commit_user_data', methods=['PUT'])
def commit_model():
    return "Commited"
