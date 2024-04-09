import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase, create_session
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class Turbo(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'Turbo'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

