# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text

from base import Base


class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)