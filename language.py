# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text

from base import Base


class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    created = Column(Date, nullable=False)
    # updated = Column(Date)

    def __init__(self, title, level, created):
        self.title = title
        self.level = level
        self.created = created
