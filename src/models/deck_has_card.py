from src import db


class DeckHasCard(db.db.Model):
    __tablename__ = 'deck_has_card'

    id_deck = db.db.Column(db.db.String(255), db.db.ForeignKey("deck.id_deck"), primary_key=True)
    id_card = db.db.Column(db.db.Integer, db.db.ForeignKey("card.id_card"), primary_key=True)
