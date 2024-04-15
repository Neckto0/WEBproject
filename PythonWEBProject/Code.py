from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class Codes(FlaskForm):
    code = TextAreaField("Введите код")
    submit = SubmitField("Проверить")