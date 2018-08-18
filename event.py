# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.orm import relationship

from base import Base

event_user_association = Table(
    'event_user', Base.metadata,
    Column('event_id', Integer, ForeignKey('event.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    event_author = Column(String)
    topic = Column(String)
    language_level = Column(Integer)
    date = Column(Date)
    max_members = Column(Integer)
    current_num_members = Column(Integer)
    created = Column(Date)
    updated = Column(Date)
    users = relationship("User", secondary=event_user_association)

    def __init__(self, topic, language_level, event_author, date, max_members, current_num_members, created, updated):
        self.topic = topic
        self.language_level = language_level
        self.event_author = event_author
        self.date = date
        self.max_members = max_members
        self.current_num_members = current_num_members
        self.created = created
        self.updated = updated