import os

from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine

from src.blueprints.auth import auth_blueprint
from src.blueprints.main import main_blueprint
from src.blueprints.user import user_blueprint
from src.models import metadata

# create and configure the app
app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

app.config['DB_USERNAME'] = os.environ.get('DB_USERNAME')
app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD')
app.config['DB_HOSTNAME'] = os.environ.get('DB_HOSTNAME')
app.config['DB_NAME'] = os.environ.get('DB_NAME')
app.config['JWT_KEY'] = os.environ.get('JWT_KEY')
app.config['EXPIRES_IN'] = os.environ.get('EXPIRES_IN')
app.config['ROOT_DECK_ID'] = os.environ.get('ROOT_DECK_ID')
app.config['ROOT_DECK_NAME'] = os.environ.get('ROOT_DECK_NAME')

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{db_username}:{db_password}@{db_hostname}/{db_name}".format(
    db_username=app.config['DB_USERNAME'], db_password=app.config['DB_PASSWORD'], db_hostname=app.config[
        'DB_HOSTNAME'], db_name=app.config['DB_NAME'])
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
conn = engine.connect()
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

metadata.create_all(engine)

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

# blueprint for parser and webhook parts of app
app.register_blueprint(main_blueprint)

# blueprint for user part of app
app.register_blueprint(user_blueprint)
