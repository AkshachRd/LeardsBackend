from src import db


class DeckHasDeck(db.db.Model):
    __tablename__ = 'deck_has_deck'

    id_parent_deck = db.db.Column(db.db.String(255), db.db.ForeignKey("deck.id_deck"), primary_key=True)
    id_child_deck = db.db.Column(db.db.String(255), db.db.ForeignKey("deck.id_deck"), primary_key=True)
