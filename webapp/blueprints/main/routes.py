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

from webapp.blueprints.main.forms import (
    Form_Card,
    Form_Board
)

from webapp.blueprints.main.models import (
    Board,
    Card
)

from webapp.blueprints.main.utils import iter_pages

main = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path='/static')


def save_file(form_file):
    if form_file:
        _, extension = os.path.splitext(form_file.filename)
        file_name = secrets.token_hex(8) + extension
        while file_name in os.listdir(os.path.join(main.root_path, 'static/assets/image')):
            file_name = secrets.token_hex(8) + extension

        if extension in ('.jpg', '.png'):
            file_path = os.path.join(main.root_path, 'static/assets/image', file_name)

        form_file.save(file_path)

        return file_name
    else:
        return ''


@main.route("/edit_card/<int:id>", methods=['GET', 'POST'])
@main.route('/create_card', methods=['GET', 'POST'])
@login_required
def create_card(id=None):
    form = Form_Card()
    form.id_board.choices = [(row.id, row.title) for row in Board.query.all()]

    if id:
        card = Card.query.get_or_404(id)

    # get values from parameters if available
    if request.method == 'GET':
        form.process(request.args)
        form.id_board.data = session.get('board', Board.query.first().id)

        if id:
            form.id_board.data = card.id_board
            form.title.data = card.title
            form.description.data = card.description
            form.image.data = card.image

    if form.validate_on_submit():
        try:
            if id:
                card.id_board = form.id_board.data
                card.title = form.title.data
                card.description = form.description.data
                card.image = save_file(form.image.data)

                db.session.commit()

                flash('Done!', 'success')
                return redirect(url_for('main.card', id=card.id))
            else:
                row = Card(
                    id_board=form.id_board.data,
                    title=form.title.data,
                    description=form.description.data,
                    image=save_file(form.image.data))
                db.session.add(row)
                db.session.commit()

                flash('Done!', 'success')
        except exc.IntegrityError as e:
            flash(f'Error: {e}', 'danger')

    return render_template(
        f'create_card.html',
        title='Create a card',
        form=form)


@main.route('/edit_board/<int:id>', methods=['GET', 'POST'])
@main.route('/create_board', methods=['GET', 'POST'])
@login_required
def create_board(id=None):
    form = Form_Board()

    if id:
        board = Board.query.get_or_404(id)

    # get values from parameters if available
    if request.method == 'GET':
        form.process(request.args)
        if id:
            form.title.data = board.title

    if form.validate_on_submit():
        try:
            if id:
                board.title = form.title.data
                db.session.commit()

                return redirect(url_for('main.board', id=id))
                flash('Done!', 'success')
            else:
                row = Board(title=form.title.data)
                db.session.add(row)
                db.session.commit()

                return redirect(url_for('main.board', id=row.id))
                flash('Done!', 'success')
        except exc.IntegrityError as e:
            flash(f'Error: {e}', 'danger')

    return render_template(
        f'create_board.html',
        title='Create a board',
        form=form)


@main.route('/board/<int:id>', methods=['GET', 'POST'])
@login_required
def board(id):
    session['board'] = id
    page = request.args.get('page', 1, type=int)
    board = Board.query.get_or_404(id)
    cards = Card.query.filter_by(board=board)\
        .paginate(per_page=10, page=page)

    return render_template(
        f'board.html',
        title='Create a board',
        data=cards,
        board=board,
        page=page)


@main.route("/card/<int:id>")
def card(id):
    session['card'] = id
    card = Card.query.get_or_404(id)
    return render_template(
        'card.html',
        title=card.title,
        card=card)


@main.route('/', methods=['GET', 'POST'])
@main.route("/boards")
def boards():
    page = request.args.get('page', 1, type=int)
    return render_template(
        'boards.html',
        title='Boards',
        data=Board.query.paginate(per_page=10, page=page))


@main.route("/delete_board/<int:id>")
def delete_board(id):
    board = Board.query.get_or_404(id)
    for card in board.cards:
        db.session.delete(card)

    db.session.delete(board)
    db.session.commit()

    return redirect(url_for('main.boards'))


@main.route("/delete_card/<int:id>")
def delete_card(id):
    card = Card.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()

    return redirect(url_for('main.board', id=session.get('board')))


