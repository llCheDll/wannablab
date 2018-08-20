# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text, Boolean

from base import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    created = Column(Date, nullable=False)
    updated = Column(Date)
    deleted = Column(Boolean)

    def __init__(self, title, created, updated, deleted):
        self.title = title
        self.created = created
        self.updated = updated
        self.deleted = deleted