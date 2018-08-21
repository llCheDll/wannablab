# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text, Boolean

from base import Base


class Friends(Base):
    __tablename__ = 'friends'

    id = Column(Integer, primary_key=True)
    friend_with = Column(Integer, nullable=False)

    def __init__(self, friend_with):
        self.friend_with = friend_with
