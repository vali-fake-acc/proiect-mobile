import secrets

from flask import url_for
from flask_mail import Message

from webapp import (
    mail,
    login_manager
)

from webapp.blueprints.users.models import User


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        'Password Reset Request',
        sender='test.lab.colors@gmail.com',
        recipients=[user.email])

    msg.body = f'''
To reset the password, click the following link:
{url_for('users.password_reset', token=token, _external=True)}

If you did not make this request, ignore this email.
'''

    mail.send(msg)
