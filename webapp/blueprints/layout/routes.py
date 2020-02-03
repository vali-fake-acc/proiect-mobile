import os
import secrets

from flask_login import login_required
from sqlalchemy import exc

from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash,
    Blueprint,
    session,
    jsonify
)

from webapp import (
    db,
    logging
)

layout = Blueprint('layout', __name__, template_folder='templates', static_folder='static', static_url_path='/static')
