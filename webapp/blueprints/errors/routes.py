from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash,
    Blueprint
)

errors = Blueprint('errors', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500

