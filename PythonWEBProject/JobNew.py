from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, FileField


class NewJob(FlaskForm):
    det_titl = TextAreaField("Name of the new part")
    type = TextAreaField("Type")
    qual = TextAreaField("Quality")
    price = TextAreaField("Price")
    picture = FileField("Picture")
    about = TextAreaField("About")
    submit = SubmitField("Submit")
