from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash

# import jwt
from functions import fetch_model, test
from models.user import User
from my_sqlalchemy import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return 'User doesn\'t exist or password is wrong', 400  # if the user doesn't exist or password is wrong,
    #token = jwt.encode({
    #    'userId': user.id_user,
    #    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
    #}, app.app.config['SECRET_KEY'])
    # if the above check passes, then we know the user has the right credentials
    return fetch_model(user)


@auth.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    username = request.form.get('name')
    password = request.form.get('password')
    phone = request.form.get('phone')

    user = User.query.filter_by(
        email=email
    ).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        return 'The user is already exists', 400

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email,
                        username=username,
                        password_hash=generate_password_hash(password, method='sha256'),
                        phone=phone
                        )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return 'Account created successfully', 200


@auth.route('/logout')
def logout():
    return test()

#def check_for_token(func):
#    @wraps(func)
#    def wrapped(*args, **kwargs):
#        token = request.args.get('token')
#        if not token:
#        try:
#            data = jwt.decode(token, app.app.config['SECRET_KEY'])
#        except:
#            return jsonify({'massage': 'Invalid token'}), 403
#        return func(*args, **kwargs)
#    return wrapped
