from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, BooleanField


class NewJob(FlaskForm):
    job_title = TextAreaField("Job Title")
    team_leader_id = TextAreaField("Team leader id")
    work_size = TextAreaField("Work size")
    collaborators = TextAreaField("Collaborators")
    is_finished = BooleanField("is job Finished?")
    submit = SubmitField("Submit")