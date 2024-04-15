from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField


class Filter(FlaskForm):
    min = StringField("Мин.")
    max = StringField("Макс.")
    fork = BooleanField("Вилка")
    breakers = BooleanField("Тормоза")
    wheels = BooleanField("Колеса")
    frame = BooleanField("Рама")
    saddle = BooleanField("Седло")
    saddle_post = BooleanField("Подседельный штырь")
    grips = BooleanField("Грипсы")
    steering_colm = BooleanField("Рулевая колонка")
    transmission = BooleanField("Трансмисия")
    stem = BooleanField("Вынос")
    bar = BooleanField("Руль")
    pedals = BooleanField("Педали")
    submit = SubmitField("Показать")