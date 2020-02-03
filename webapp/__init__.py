from flask import (
    Flask,
    redirect,
    url_for
)

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from webapp.config import Config

import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from webapp.blueprints.layout.routes import layout
from webapp.blueprints.users.routes import users
from webapp.blueprints.main.routes import main
from webapp.blueprints.errors.routes import errors

app.register_blueprint(layout, url_prefix='/layout')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(main, url_prefix='/main')
app.register_blueprint(errors, url_prefix='/errors')


@app.route('/')
def index():
    return redirect(url_for('main.boards'))
