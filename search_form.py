from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    query_field = StringField(validators=[InputRequired()])
    submit = SubmitField('Find')
