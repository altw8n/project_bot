import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    photo_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    '''modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    signup = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)'''