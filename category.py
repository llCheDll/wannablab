# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text

from base import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)