from src.db import db


class Deck(db.Model):
    __tablename__ = 'deck'

    id_deck = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    background = db.Column(db.String(255), nullable=False)  # TODO: boolean

    def __init__(self, name, background):
        self.name = name
        self.background = background
