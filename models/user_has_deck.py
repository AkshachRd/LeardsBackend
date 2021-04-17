from my_sqlalchemy import db


class UserHasDeck(db.Model):
    __tablename__ = 'user_has_deck'

    id_user = db.Column(db.String(255), db.ForeignKey("user.id_user"), primary_key=True)
    id_root_deck = db.Column(db.String(255), db.ForeignKey("deck.id_deck"), primary_key=True)
