from flask import jsonify

from src.models.card import Card
from src.models.deck import Deck
from src.models.deck_has_card import DeckHasCard
from src.models.deck_has_deck import DeckHasDeck

from src.models.user import User
from src.models.user_has_deck import UserHasDeck


def fetch_model(user_id):
    user = User.query.filter_by(id_user=user_id).first()
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

    user_decks = UserHasDeck.query.filter_by(id_user=user.id_user).all()
    for user_deck in user_decks:
        model['dataState']['rootGroup']['content'].append(extract_deck(user_deck.id_root_deck, 'root'))

    return jsonify(model)


def extract_deck(deck_id, parent_deck_id):
    deck = Deck.query.get(deck_id)
    model_deck = {
        'id': deck_id,
        'parentId': parent_deck_id,
        'name': deck.name,
        'img': deck.background,
        'content': []
    }

    nested_decks = DeckHasDeck.query.filter_by(id_parent_deck=deck_id).all()
    if nested_decks:
        for nested_deck in nested_decks:
            model_deck['content'].append(extract_deck(nested_deck.id_child_deck, nested_deck.id_parent_deck))
    else:
        model_deck['content'] = extract_cards(deck_id)

    return model_deck


def extract_cards(deck_id):
    cards = []

    decks_with_cards = DeckHasCard.query.filter_by(id_deck=deck_id).all()
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

    card = Card.query.filter_by(id_card=deck_with_card.id_card).first()
    model_card['id'] = card.id_card
    model_card['word'] = card.front_text
    model_card['partOfSpeech']['noun']['translation'] = card.back_text

    return model_card
