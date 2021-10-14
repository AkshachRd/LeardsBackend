from sqlalchemy import select
from enum import Enum
from flask import jsonify
import src.app as app_file

from src.models import card as card_table, deck as deck_table, deck_has_card as deck_has_card_table,\
    deck_has_deck as deck_has_deck_table, user_has_deck as user_has_deck_table


class ContentType(str, Enum):
    DECKS = "decks"
    CARDS = "cards"
    NO_CONTENT = "no-content"


def fetch_user_model(user_id):
    """Extract user's model from DB

    :param user_id:
    :type user_id: str
    :return: User model
    :rtype: dict
    """
    model = {
        'id': app_file.app.config['ROOT_DECK_ID'],
        'name': app_file.app.config['ROOT_DECK_NAME'],
        'content': [],
        'contentType': ContentType.DECKS
    }

    stmt = (
        select([user_has_deck_table]).
        where(user_has_deck_table.c.id_user == user_id)
    )
    user_decks = app_file.conn.execute(stmt).fetchall()

    if user_decks:
        for user_deck in user_decks:
            model['content'].append(extract_deck(user_deck.id_root_deck))

    return model


def extract_deck(deck_id):
    """Extract a deck from DB

    :param deck_id:
    :type deck_id: str
    :return: Deck of decks or cards
    :rtype: dict
    """
    stmt = (
        select([deck_table]).
        where(deck_table.c.id_deck == deck_id)
    )
    deck = app_file.conn.execute(stmt).first()

    model_deck = {
        'id': deck_id,
        'name': deck.name,
        'content': [],
        'contentType': ContentType.DECKS
    }

    stmt = (
        select([deck_has_deck_table]).
        where(deck_has_deck_table.c.id_parent_deck == deck_id)
    )
    nested_decks = app_file.conn.execute(stmt).fetchall()

    if nested_decks:
        model_deck['contentType'] = ContentType.DECKS
        for nested_deck in nested_decks:
            model_deck['content'].append(extract_deck(nested_deck.id_child_deck))
    else:
        model_deck['contentType'] = ContentType.CARDS
        model_deck['content'] = extract_cards(deck_id)

    return model_deck


def extract_cards(deck_id):
    """Extract deck cards from DB

    :param deck_id:
    :type deck_id: str
    :return: List of cards
    :rtype: list
    """
    cards = []

    stmt = (
        select([deck_has_card_table]).
        where(deck_has_card_table.c.id_deck == deck_id)
    )
    decks_with_cards = app_file.conn.execute(stmt).fetchall()

    if decks_with_cards:
        for deck_with_card in decks_with_cards:
            cards.append(extract_card(deck_with_card.id_card))

    return cards


def extract_card(card_id):
    """Extract a card from DB

    :param card_id:
    :type card_id: str
    :return: Card
    :rtype: dict
    """
    model_card = {
        'id': '',
        'word': '',
        'translations': []
    }

    stmt = (
        select([card_table]).
        where(card_table.c.id_card == card_id)
    )
    card = app_file.conn.execute(stmt).first()

    model_card['id'] = card.id_card
    model_card['word'] = card.front_text
    model_card['translations'] = [card.back_text]

    return model_card


def commit_user_model(user_id, model):
    """Extract user's model from DB

    :param user_id:
    :type user_id: str
    :return: User model
    :rtype: dict
    """

    if not (model.get('id') == app_file.app.config['ROOT_DECK_ID']
            and model.get('name') == app_file.app.config['ROOT_DECK_NAME']
            and model.get('contentType') == ContentType.DECKS):
        return jsonify(), 400

    stmt = (
        select([user_has_deck_table]).
        where(user_has_deck_table.c.id_user == user_id)
    )
    user_decks = app_file.conn.execute(stmt).fetchall()

    if user_decks:
        for user_deck in user_decks:
            model['content'].append(extract_deck(user_deck.id_root_deck))

    return model
