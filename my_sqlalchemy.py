from flask_sqlalchemy import SQLAlchemy

from settings import DB_NAME, DB_HOSTNAME, DB_PASSWORD, DB_USERNAME

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{db_username}:{db_password}@{db_hostname}/{db_name}".format(
    db_username=DB_USERNAME, db_password=DB_PASSWORD, db_hostname=DB_HOSTNAME, db_name=DB_NAME
)

db = SQLAlchemy()