from my_sqlalchemy import db


class User(db.Model):
    __tablename__ = "user"

    id_user = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))
    # model = db.Column(db.JSON, nullable=False)