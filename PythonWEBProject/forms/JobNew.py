from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, FileField, SelectField


class NewJob(FlaskForm):
    det_titl = TextAreaField("Name of the new part")
    type = SelectField("Type", choices=[(1, "Вилка"), (2, "Тормоза"), (3, "Колеса"),
                                        (4, "Рама"), (5, "Седло"), (6, "Подседельный штырь"),
                                        (7, "Грипсы"), (8, "Рулевая колонка"), (9, "Трансмисия"),
                                        (10, "Вынос"), (11, "Руль"), (12, "Педали"),
                                        (13, "Велосипед в сборе")])
    qual = TextAreaField("Quality")
    price = TextAreaField("Price")
    picture = FileField("Picture", name="pic")
    about = TextAreaField("About")
    submit = SubmitField("Submit")
