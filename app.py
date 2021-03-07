from sqlalchemy.dialects.mysql import INTEGER
from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from settings import DB_NAME, DB_HOSTNAME, DB_PASSWORD, DB_USERNAME

import os

from auth import auth as auth_blueprint
from main import main as main_blueprint

# create and configure the app
app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{db_username}:{db_password}@{db_hostname}/{db_name}".format(
    db_username=DB_USERNAME, db_password=DB_PASSWORD, db_hostname=DB_HOSTNAME, db_name=DB_NAME
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"

    id_user = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))


class Deck(db.Model):
    __tablename__ = "deck"

    id_deck = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    background = db.Column(db.String(255), nullable=False)


class Card(db.Model):
    __tablename__ = "card"

    id_card = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    front_text = db.Column(db.String(255), nullable=False)
    back_text = db.Column(db.String(255), nullable=False)


class Deck_has_card(db.Model):
    __tablename__ = "deck_has_card"

    id_deck = db.Column(INTEGER(unsigned=True), db.ForeignKey("deck.id_deck"), primary_key=True)
    id_card = db.Column(INTEGER(unsigned=True), db.ForeignKey("card.id_card"), primary_key=True)


class User_has_deck(db.Model):
    __tablename__ = "user_has_deck"

    id_user = db.Column(INTEGER(unsigned=True), db.ForeignKey("user.id_user"), primary_key=True)
    id_deck = db.Column(INTEGER(unsigned=True), db.ForeignKey("deck.id_deck"), primary_key=True)


app.config['CORS_HEADERS'] = 'Content-Type'
#app.config.from_mapping(
#    SECRET_KEY='dev',
#    DATABASE=SQLALCHEMY_DATABASE_URI,
#)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# blueprint for auth routes in our app


app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app


app.register_blueprint(main_blueprint)
