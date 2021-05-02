from src import db


class Deck(db.db.Model):
    __tablename__ = 'deck'

    id_deck = db.db.Column(db.db.String(255), primary_key=True)
    name = db.db.Column(db.db.String(255), nullable=False)
    background = db.db.Column(db.db.String(255), nullable=False)

    def __init__(self, name, background):
        self.name = name
        self.background = background
