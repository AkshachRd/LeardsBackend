from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from settings import DB_NAME, DB_HOSTNAME, DB_PASSWORD, DB_USERNAME
import os

from auth import auth as auth_blueprint
from main import main as main_blueprint


SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{db_username}:{db_password}@{db_hostname}/{db_name}".format(
    db_username=DB_USERNAME, db_password=DB_PASSWORD, db_hostname=DB_HOSTNAME, db_name=DB_NAME
)

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
CORS(app)

db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=SQLALCHEMY_DATABASE_URI,
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# blueprint for auth routes in our app


app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app


app.register_blueprint(main_blueprint)
