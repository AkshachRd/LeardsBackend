from flask import Flask, redirect, url_for, request
from flask_cors import CORS, cross_origin
from wordParser import parse_word
from flask_sqlalchemy import SQLAlchemy
from settings import *
import json
import git
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{db_username}:{db_password}@{db_hostname}/{db_name}".format(
        db_username=DB_USERNAME, db_password=DB_PASSWORD, db_hostname=DB_HOSTNAME, db_name=DB_NAME
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = SQLAlchemy(app)

    cors = CORS(app, resources={r"/": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    # a simple page that says hello
    @app.route('/', methods=['POST'])
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    def get_word_example():
        if request.method == 'POST':
            word = request.json['word']
            return json.dumps(parse_word(word))

    @app.route('/webhook', methods=['POST'])
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    def webhook():
        if request.method == 'POST':
            repo = git.Repo('./LeardsBackend')
            origin = repo.remotes.origin
            origin.pull()
            os.system('cmd /c "python -m pip install -r requirements.txt"')

            return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Wrong event type', 400

    return app
