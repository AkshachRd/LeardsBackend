from sqlalchemy import MetaData, Table, Column, String, ForeignKey
import uuid

metadata = MetaData()

card = Table('card', metadata,
             Column('id_card', String(36), default=str(uuid.uuid4()), primary_key=True),
             Column('front_text', String(255), nullable=False),
             Column('back_text', String(255), nullable=False)
             )

deck = Table('deck', metadata,
             Column('id_deck', String(36), default=str(uuid.uuid4()), primary_key=True),
             Column('name', String(255), nullable=False),
             )

deck_has_card = Table('deck_has_card', metadata,
                      Column('id_deck', String(36), ForeignKey("deck.id_deck"), primary_key=True),
                      Column('id_card', String(36), ForeignKey("card.id_card"), primary_key=True)
                      )

deck_has_deck = Table('deck_has_deck', metadata,
                      Column('id_parent_deck', String(36), ForeignKey("deck.id_deck"), primary_key=True),
                      Column('id_child_deck', String(36), ForeignKey("deck.id_deck"), primary_key=True)
                      )

user = Table('user', metadata,
             Column('id_user', String(36), default=str(uuid.uuid4()), primary_key=True),
             Column('username', String(64), index=True, nullable=False),
             Column('email', String(255), index=True, unique=True, nullable=False),
             Column('password_hash', String(128), nullable=False)  # TODO: character(n)
             )

user_has_deck = Table('user_has_deck', metadata,
                      Column('id_user', String(36), ForeignKey("user.id_user"), primary_key=True),
                      Column('id_root_deck', String(36), ForeignKey("deck.id_deck"), primary_key=True)
                      )
