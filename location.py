# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text

from base import Base


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)