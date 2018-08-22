# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text, Boolean

from base import Base


class Friends(Base):
    __tablename__ = 'friends'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id
