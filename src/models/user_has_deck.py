from src import db


class UserHasDeck(db.db.Model):
    __tablename__ = 'user_has_deck'

    id_user = db.db.Column(db.db.Integer, db.db.ForeignKey("user.id_user"), primary_key=True)
    id_root_deck = db.db.Column(db.db.String(255), db.db.ForeignKey("deck.id_deck"), primary_key=True)
