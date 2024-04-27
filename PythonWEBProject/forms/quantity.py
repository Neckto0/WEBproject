from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange, DataRequired


class Quant(FlaskForm):
    quant = IntegerField("Количество товара", validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField("Сохранить")