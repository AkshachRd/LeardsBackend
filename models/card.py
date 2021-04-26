from db import db


class Card(db.Model):
    __tablename__ = 'card'

    id_card = db.Column(db.Integer, autoincrement=True, primary_key=True)
    front_text = db.Column(db.String(255), nullable=False)
    back_text = db.Column(db.String(255), nullable=False)

    def __init__(self, front_text, back_text):
        self.front_text = front_text
        self.back_text = back_text
