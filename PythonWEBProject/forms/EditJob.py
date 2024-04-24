from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, BooleanField


class EJobs(FlaskForm):
    tm = TextAreaField("Team Leader")
    job = TextAreaField("Name of job")
    work_size = TextAreaField("Work size")
    collab = TextAreaField("Collaborators")
    is_fin = BooleanField("is Finihed")
    submit = SubmitField("Submit")