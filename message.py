# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text

from base import Base


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)