import os

from flask import Flask
from flask_cors import CORS

from blueprints.auth import auth as auth_blueprint
from blueprints.main import main as main_blueprint
from my_sqlalchemy import SQLALCHEMY_DATABASE_URI, db

import models.user, models.deck, models.user_has_deck, models.deck_has_card, models.card, models.deck_has_deck
# create and configure the app
app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

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
