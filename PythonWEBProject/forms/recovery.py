from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired


class Recov(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    submit = SubmitField("Продолжить")
