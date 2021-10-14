import datetime

import src.app as app_file
import jwt


def create_token(user_id, expires_in):
    token = jwt.encode({
        'userId': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }, app_file.app.config['JWT_KEY'], algorithm="HS256")

    return token


def get_user_id_from_token(token):
    """

    :param token:
    :type: str
    :return: If the token is expired, it will return None, otherwise user id
    :rtype: None | str
    """
    if not token:
        return None

    try:
        data = jwt.decode(token, app_file.app.config['JWT_KEY'], algorithms="HS256")
        return data['userId']
    except jwt.exceptions.ExpiredSignatureError:
        return None
