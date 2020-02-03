from datetime import datetime
from webapp import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_board = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    creat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modificat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.Text)

    def __repr__(self):
        return f'''Card({self.id}, {self.id_board}, "{self.title}", "{self.description}", "{self.image}")'''


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modificat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    title = db.Column(db.Text, nullable=False)

    cards = db.relationship("Card", backref=db.backref('board', lazy=True), lazy=True)

    def __repr__(self):
        return f'''Board({self.id}, "{self.title}")'''

