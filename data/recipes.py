from sqlalchemy import orm, Integer, String, Column, ForeignKey, Boolean
from sqlalchemy.types import JSON
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime as dt
from .db_session import SqlAlchemyBase


class Recipe(SqlAlchemyBase, SerializerMixin):  # модель рецепта
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=True)
    author = Column(Integer, ForeignKey("users.id"), nullable=True)
    prep_time = Column(Integer, nullable=True)
    tags = Column(JSON, nullable=True)
    date = Column(String, default=dt.strftime(dt.now(), "%b %d, %Y"))
    description = Column(String, nullable=True)
    ingredients = Column(JSON, nullable=True)
    image_url = Column(String, nullable=True)
    cropped_image_url = Column(String, nullable=True)
    cotw = Column(Boolean, nullable=True)
    views_count = Column(Integer, nullable=True)
    likes_count = Column(Integer, nullable=True)
    likers = Column(JSON, nullable=True, default="[]")
    user = orm.relation('User', foreign_keys=[author])
