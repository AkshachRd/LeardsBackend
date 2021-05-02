from src.db import db


class DeckHasDeck(db.Model):
    __tablename__ = 'deck_has_deck'

    id_parent_deck = db.Column(db.String(255), db.ForeignKey("deck.id_deck"), primary_key=True)
    id_child_deck = db.Column(db.String(255), db.ForeignKey("deck.id_deck"), primary_key=True)
