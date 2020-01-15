from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class NuovoAbbonato(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cell = StringField('Cell', validators=[DataRequired()])
    scadenza = DateField('Scadenza', format='%Y-%m-%d')
    quota = StringField('Quota', validators=[DataRequired()])
    versato = StringField('Versato', default=0)
    note = StringField('Note')
    submit = SubmitField('Pubblica')