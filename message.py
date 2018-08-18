# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text, Boolean

from base import Base


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    sender = Column(Integer, nullable=False) # FK
    receiver = Column(Integer, nullable=False) # FK M2M
    text = Column(Text, nullable=False)
    created = Column(Date, nullable=False)
    received = Column(Boolean, nullable=False)
    updated = Column(Date)
    deleted = Column(Boolean)

    def __init__(self, sender, receiver, text, created, received, updated, deleted):
        self.sender = sender
        self.receiver = receiver
        self.text = text
        self.created = created
        self.received = received
        self.updated = updated
        self.deleted = deleted