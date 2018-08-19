# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text, Boolean, ForeignKey

from base import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    # recipient = FK M2M
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    created = Column(Date, nullable=False)
    updated = Column(Date)
    deleted = Column(Boolean)

    def __init__(self, text, created, updated, deleted):
        self.text = text
        self.created = created
        self.updated = updated
        self.deleted = deleted