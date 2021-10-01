from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from src.services.user import fetch_user_model

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/fetch_model', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def fetch_model():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'message': 'The user\'s id was not provided'}), 400

    model = fetch_user_model(user_id)

    return jsonify({'models': model}), 200


@user_blueprint.route('/commit_model', methods=['PUT'])
@cross_origin(origin='*', headers=['Content-Type'])
def commit_model():
    return "Commited"
