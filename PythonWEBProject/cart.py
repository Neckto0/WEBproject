from flask_wtf import FlaskForm
from wtforms import SubmitField


class Card(FlaskForm):
    buton = SubmitField("Button")