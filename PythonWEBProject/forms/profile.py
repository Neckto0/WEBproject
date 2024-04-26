from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField


class Profile(FlaskForm):
    email = StringField("Email")
    name = StringField("Name")
    about = TextAreaField("About")
    submit = SubmitField("Config")
