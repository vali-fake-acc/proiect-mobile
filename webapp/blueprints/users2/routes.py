import json

from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
    Blueprint
)

from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

from webapp import db, bcrypt
from webapp.blueprints.users.models import User
from webapp.blueprints.users.forms import (
    Form_Registration,
    Form_Login,
    Form_Update_Password,
    Form_Password_Reset,
    Form_Request_Password_Reset
)

from webapp.blueprints.users.utils import send_reset_email

users = Blueprint('users', __name__, template_folder='templates', static_folder='static', static_url_path='/static')


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.board'))

    form = Form_Registration()
    if form.validate_on_submit():
        pw = form.password.data.encode('utf-8')
        user = User(
            email=form.email.data,
            password=bcrypt.generate_password_hash(pw).decode('utf-8'))
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.board'))

    form = Form_Login()
    with open('data/user.json') as f:
        data = json.load(f)
        for item in data.get('items'):
            form.email.data = item.get('email')
            form.password.data = item.get('password')

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)

            flash('Login successful!', 'success')
            return redirect(request.args.get('next', url_for('main.board')))
        else:
            flash('Login unsuccessful!', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = Form_Update_Password()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            pw = form.new_password.data.encode('utf-8')
            current_user.password = bcrypt.generate_password_hash(pw).decode('utf-8')
            db.session.commit()

            flash('The password has been changed!', 'success')
            return redirect(request.args.get('next', url_for('main.board')))
        else:
            flash('The password hasn\'t been changed!', 'danger')
    return render_template('account.html', title='Account', form=form)


@users.route('/request_password_reset', methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.board'))

    form = Form_Request_Password_Reset()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Check your email inbox for a link to reset the password', 'info')
        return redirect(url_for('users.login'))

    return render_template(
        'request_password_reset.html',
        title='Request Password Reset',
        form=form)


@users.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.board'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('The token is either invalid or expired.', 'warning')
        return redirect(url_for('users.request_password_reset'))

    form = Form_Password_Reset()
    if form.validate_on_submit():
        pw = form.password.data.encode('utf-8')
        user.password = bcrypt.generate_password_hash(pw).decode('utf-8')
        db.session.commit()

        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login'))
    return render_template('password_reset.html', title='Reset Password', form=form)
