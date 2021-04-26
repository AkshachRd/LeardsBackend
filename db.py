from flask_sqlalchemy import SQLAlchemy
import app

# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{db_username}:{db_password}@{db_hostname}/{db_name}".format(
# db_username=app.app.config['DB_USERNAME'], db_password=app.app.config['DB_PASSWORD'], db_hostname=app.app.config[
# 'DB_HOSTNAME'], db_name=app.app.config['DB_NAME'] )

SQLALCHEMY_DATABASE_URI = "postgresql://akshachrd:6zM6IOoLDfV3P3vHqdmt@localhost:5432/leards_db"  # .format(
#    db_username=DB_USERNAME, db_password=DB_PASSWORD, db_hostname=DB_HOSTNAME, db_name=DB_NAME
#)

db = SQLAlchemy()
