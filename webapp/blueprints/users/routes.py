import json

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from webapp import db, bcrypt, login_manager
from webapp.blueprints.users.models import User
from webapp.blueprints.users.forms import Form_Registration, Form_Login, Form_Update_Password

users = Blueprint('users', __name__, template_folder='templates', static_folder='static', static_url_path='/static')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.boards'))

    form = Form_Registration()
    if form.validate_on_submit():
        pw = form.password.data.encode('utf-8')
        user = User(email=form.email.data, password=bcrypt.generate_password_hash(pw).decode('utf-8'))
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.boards'))

    form = Form_Login()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)

            flash('Login successful!', 'success')
            return redirect(request.args.get('next', url_for('main.boards')))
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
            return redirect(request.args.get('next', url_for('main.boards')))
        else:
            flash('The password hasn\'t been changed!', 'danger')
    return render_template('account.html', title='Account', form=form)

