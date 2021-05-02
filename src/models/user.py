from src import db


class User(db.db.Model):
    __tablename__ = 'user'

    id_user = db.db.Column(db.db.Integer, primary_key=True, autoincrement=True)
    username = db.db.Column(db.db.String(64), index=True, unique=True, nullable=False)
    email = db.db.Column(db.db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.db.Column(db.db.String(128), nullable=False)
    phone = db.db.Column(db.db.String(20))

    def __init__(self, username, email, password_hash, phone):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.phone = phone
