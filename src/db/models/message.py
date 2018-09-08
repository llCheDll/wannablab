# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)

    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    author = relationship("User", foreign_keys=[author_id])
    recipient = relationship("User", foreign_keys=[recipient_id])

    text = Column(Text, nullable=False)

    created = Column(Date, nullable=False)
    updated = Column(Date)

    received = Column(Boolean, nullable=False)
    deleted = Column(Boolean)

    def __init__(self, text, author_id, recipient_id, created):
        self.text = text
        self.author_id = author_id
        self.recipient_id = recipient_id
        self.created = created
        self.updated = None
        self.received = False
        self.deleted = False
