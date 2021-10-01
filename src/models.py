from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

metadata = MetaData()

card = Table('card', metadata,
             Column('id_card', Integer, autoincrement=True, primary_key=True),
             Column('front_text', String(255), nullable=False),
             Column('back_text', String(255), nullable=False)
             )

deck = Table('deck', metadata,
             Column('id_deck', String(255), primary_key=True),
             Column('name', String(255), nullable=False),
             )

deck_has_card = Table('deck_has_card', metadata,
                      Column('id_deck', String(255), ForeignKey("deck.id_deck"), primary_key=True),
                      Column('id_card', Integer, ForeignKey("card.id_card"), primary_key=True)
                      )

deck_has_deck = Table('deck_has_deck', metadata,
                      Column('id_parent_deck', String(255), ForeignKey("deck.id_deck"), primary_key=True),
                      Column('id_child_deck', String(255), ForeignKey("deck.id_deck"), primary_key=True)
                      )

user = Table('user', metadata,
             Column('id_user', Integer, autoincrement=True, primary_key=True),
             Column('username', String(64), index=True, unique=True, nullable=False),
             Column('email', String(255), index=True, unique=True, nullable=False),
             Column('password_hash', String(128), nullable=False)  # TODO: character(n)
             )

user_has_deck = Table('user_has_deck', metadata,
                      Column('id_user', Integer, ForeignKey("user.id_user"), primary_key=True),
                      Column('id_root_deck', String(255), ForeignKey("deck.id_deck"), primary_key=True)
                      )
