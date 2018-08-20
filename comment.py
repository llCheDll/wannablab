# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    author = relationship("User", foreign_keys=[author_id])
    recipient = relationship("User", foreign_keys=[recipient_id])
    
    text = Column(Text, nullable=False)
    created = Column(Date, nullable=False)
    updated = Column(Date)
    deleted = Column(Boolean)

    def __init__(self, author_id, recipient_id, text, created, updated, deleted):
        self.author_id = author_id
        self.recipient_id = recipient_id
        self.text = text
        self.created = created
        self.updated = updated
        self.deleted = deleted
