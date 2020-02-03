import sys
import json
import time
from pprint import pprint

from flask import request
from flask_bcrypt import Bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from webapp import db
from webapp.blueprints.users.models import User

from webapp.blueprints.main.models import (
    Board,
    Card
)

from webapp.blueprints.main.utils import iter_pages

bcrypt = Bcrypt()


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'r':
            db_reset(create=True, pr=True)
        elif sys.argv[1] == 'rr':
            db_reset(create=False, pr=True)
    else:
        pprint(Card.query.all())
        pprint(Board.query.all())


def db_reset(create=False, pr=False):
    db.drop_all()
    db.create_all()

    if create:
        create_user(pr)
        create_board(pr)
        create_card(pr)


def create_board(pr):
    print('\ncreate_board()')
    with open('data/board.json', 'r') as f:
        data = json.load(f)
        for item in data.get('items'):
            row = Board(title=item.get('title', ''))
            db.session.add(row)
            db.session.commit()

            if pr in (True, 'board'):
                print(row)


def create_card(pr):
    print('\ncreate_card()')
    with open('data/card.json', 'r') as f:
        data = json.load(f)
        for item in data.get('items'):
            row = Card(
                title=item.get('title', ''),
                description=item.get('description', ''),
                image=item.get('image', ''),
                id_board=1)
            db.session.add(row)
            db.session.commit()

            if pr in (True, 'card'):
                print(row)


def create_user(pr):
    print('\ncreate_user()')
    with open('data/user.json', 'r') as f:
        data = json.load(f)
        for item in data.get('items'):
            row = User(
                email=item.get('email'),
                password=bcrypt.generate_password_hash(item.get('password')))
            db.session.add(row)
            db.session.commit()

            if pr in (True, 'user'):
                print(row)


if __name__ == '__main__':
    main()

