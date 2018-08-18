# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text

from base import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)