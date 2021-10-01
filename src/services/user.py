from flask import jsonify
from sqlalchemy import select
import src.app as app

from src.models import card as card_table, deck as deck_table, deck_has_card as deck_has_card_table, deck_has_deck as deck_has_deck_table, user as user_table, user_has_deck as user_has_deck_table


def fetch_user_model(user_id):
    stmt = (
        select([user_table]).
        where(user_table.c.id_user == user_id)
    )
    user = app.conn.execute(stmt).first()
    model = {
        'user': {
            'id': user.id_user,
            'name': user.username,
            'email': user.email,
            'profileImage': 'https://images-ext-2.discordapp.net/external/_JtzjmdL5US9Fx2SoC_CCovQEwadWq_Zj3SYASN6ihw'
                            '/https/i.ibb.co/DR067K7/Group-241-1.png%27 '
        },
        'dataState': {
            'currentGroupId': 'root',
            'rootGroup': {
                'id': 'root',
                'parentId': 'root',
                'name': 'decks',
                'img': '',
                'content': []
            }
        }
    }

    stmt = (
        select([user_has_deck_table]).
        where(user_has_deck_table.c.id_user == user.id_user)
    )
    user_decks = app.conn.execute(stmt)
    for user_deck in user_decks:
        model['dataState']['rootGroup']['content'].append(extract_deck(user_deck.id_root_deck, 'root'))

    return jsonify(model)


def extract_deck(deck_id, parent_deck_id):
    stmt = (
        select([deck_table]).
        where(deck_table.c.id_deck == deck_id).first()
    )
    deck = app.conn.execute(stmt)

    model_deck = {
        'id': deck_id,
        'parentId': parent_deck_id,
        'name': deck.name,
        'img': deck.background,
        'content': []
    }

    stmt = (
        select([deck_has_deck_table]).
        where(deck_has_deck_table.c.id_parent_deck == deck_id)
    )
    nested_decks = app.conn.execute(stmt)

    if nested_decks:
        for nested_deck in nested_decks:
            model_deck['content'].append(extract_deck(nested_deck.id_child_deck, nested_deck.id_parent_deck))
    else:
        model_deck['content'] = extract_cards(deck_id)

    return model_deck


def extract_cards(deck_id):
    cards = []

    stmt = (
        select([deck_has_card_table]).
        where(deck_has_card_table.c.id_deck == deck_id)
    )
    decks_with_cards = app.conn.execute(stmt)

    if decks_with_cards:
        for deck_with_card in decks_with_cards:
            cards.append(extract_card(deck_with_card))

    return cards


def extract_card(deck_with_card):
    model_card = {
        'id': '',
        'word': '',
        'pronunciation': {
            'audioUK': '',
            'audioUS': '',
            'transcriptionUK': '',
            'transcriptionUS': ''
        },
        'partOfSpeech': {
            'noun': {
                'definitions': [],
                'derivedTerms': [],
                'meronyms': [],
                'plural': '',
                'translation': ''
            },
            'verb': {
                'definitions': [],
                'pastParticiple': '',
                'pastSimple': '',
                'presentSimple': '',
                'translation': ''
            }
        }
    }

    stmt = (
        select([card_table]).
        where(card_table.c.id_card == deck_with_card.id_card)
    )
    card = app.conn.execute(stmt).first()

    model_card['id'] = card.id_card
    model_card['word'] = card.front_text
    model_card['partOfSpeech']['noun']['translation'] = card.back_text

    return model_card
