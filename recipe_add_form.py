from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from PIL import Image


class RecipeAddForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    prep_time = IntegerField('Время приготовления, мин', validators=[DataRequired()])
    tags = StringField('Теги (через запятую)', validators=[DataRequired()])
    description = TextAreaField('Desciption', validators=[DataRequired()])
    ingredients = StringField('Ингредиенты (через запятую)', validators=[DataRequired()])
    image = FileField('photo (1000 x 1000)', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Отправить')


def validate_img(flaskform, field):
    if check_img_size(field.data):
        raise ValidationError("Uploaded picture is too small")


def check_img_size(form_header_picture):
    i = Image.open(form_header_picture)
    if (i.size[0] < 1000) and (i.size[1] < 1000):
        return True
