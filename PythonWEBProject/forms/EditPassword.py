from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash, generate_password_hash


class EditPass(FlaskForm):
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_ag = PasswordField("Повторите пороль", validators=[DataRequired()])
    submit = SubmitField("Изменить")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
