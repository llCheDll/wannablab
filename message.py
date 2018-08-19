# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base

# message_user_association = Table(
#     'message_user', Base.metadata,
#     Column('message_id', Integer, ForeignKey('message.id')),
#     Column('user_id', Integer, ForeignKey('user.id'))
# )

class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    # receiver = Column(String)
    # receiver = relationship("User", backref=backref("message", uselist=False))
    # sender = Column(Integer, ForeignKey('user.id'))
    text = Column(Text, nullable=False)
    created = Column(Date, nullable=False)
    received = Column(Boolean, nullable=False)
    updated = Column(Date)
    deleted = Column(Boolean)

    def __init__(self, text, created, received, updated, deleted):
        # self.sender = self # sender
        # self.receiver = receiver
        self.text = text
        self.created = created
        self.received = received
        self.updated = updated
        self.deleted = deleted