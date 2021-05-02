from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{db_username}:{db_password}@{db_hostname}/{db_name}".format(
    db_username=app.app.config['DB_USERNAME'], db_password=app.app.config['DB_PASSWORD'], db_hostname=app.app.config[
        'DB_HOSTNAME'], db_name=app.app.config['DB_NAME'])

db = SQLAlchemy()
