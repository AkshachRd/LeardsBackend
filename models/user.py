from my_sqlalchemy import db


class User(db.Model):
    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))

    def __init__(self, id_user, username, email, password_hash, phone):
        self.id_user = id_user
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.phone = phone
