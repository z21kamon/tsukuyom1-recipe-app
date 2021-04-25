from flask_wtf import FlaskForm
from wtforms import SubmitField


class LikeButton(FlaskForm):
    like = SubmitField('like')


class DislikeButton(FlaskForm):
    like = SubmitField('dislike')
