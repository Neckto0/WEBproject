from flask import Blueprint, jsonify
from . import db_session
from .users import User

us_bl_print = Blueprint(
    "users",
    __name__,
    template_folder="templates"
)


@us_bl_print.route("/api/users", methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users': [us.to_dict(only=('email', 'name', 'about'))
                      for us in users]
        }
    )