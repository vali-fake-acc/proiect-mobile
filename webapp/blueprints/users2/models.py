from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from webapp import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def get_reset_token(self, minutes_before_expiry=30):
        serializer = Serializer(current_app.config.get('SECRET_KEY'), minutes_before_expiry * 60)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(current_app.config.get('SECRET_KEY'))
        try:
            user_id = serializer.loads(token).get('user_id')
            return User.query.get(user_id)
        except Exception as e:
            print('ERROR: The token has expired!')
            return None

    def __repr__(self):
        return f'''User({self.id}, "{self.email}", {self.password})'''
