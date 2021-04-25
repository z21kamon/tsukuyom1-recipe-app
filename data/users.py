from sqlalchemy import orm, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
import datetime


class User(SqlAlchemyBase, UserMixin, SerializerMixin):  # модель пользователя
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, nullable=True, unique=True)
    age = Column(Integer, nullable=True)
    country = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    last_online = Column(DateTime, default=datetime.datetime.now)
    recipes = Column(String, ForeignKey("recipes.id"), nullable=True)
    recipe = orm.relation('Recipe', foreign_keys=[recipes])

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
