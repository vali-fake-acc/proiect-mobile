from flask_wtf import FlaskForm
from wtforms.validators import InputRequired

from wtforms import (
    StringField,
    SelectField,
    SubmitField,
)

from flask_wtf.file import (
    FileField,
    FileAllowed
)


class Form_Card(FlaskForm):
    id_board = SelectField('Board', coerce=int, validators=[InputRequired()])
    title = StringField('Title', validators=[InputRequired()])
    description = StringField('Description')
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png']), InputRequired()])

    submit = SubmitField('Add')


class Form_Board(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    submit = SubmitField('Add')

