from my_sqlalchemy import db


class Card(db.Model):
    __tablename__ = "card"

    id_card = db.Column(db.Integer, primary_key=True)
    front_text = db.Column(db.String(255), nullable=False)
    back_text = db.Column(db.String(255), nullable=False)