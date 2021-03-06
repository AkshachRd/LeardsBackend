from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from settings import *
import os

db = SQLAlchemy()
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{db_username}:{db_password}@{db_hostname}/{db_name}".format(
        db_username=DB_USERNAME, db_password=DB_PASSWORD, db_hostname=DB_HOSTNAME, db_name=DB_NAME
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)


    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    cors = CORS(app, resources={r"/": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=SQLALCHEMY_DATABASE_URI,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
