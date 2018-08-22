# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, Text
from sqlalchemy.orm import relationship

from base import Base

event_members_association = Table(
    'event_members', Base.metadata,
    Column('event_id', Integer, ForeignKey('event.id')),
    Column('member_id', Integer, ForeignKey('user.id')),
    # Column('member_status', Bool )
)


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    
    author_id = Column(Integer, ForeignKey('user.id'))
    event_author = relationship("User")
    
    topic = Column(String)
    description = Column(Text)
    
    language_id = Column(Integer, ForeignKey('language.id'))
    language = relationship("Language")
    
    date = Column(Date, nullable=False)
    
    max_members = Column(Integer, nullable=False)
    current_num_members = Column(Integer) # ???
    
    created = Column(Date, nullable=False)
    updated = Column(Date)

    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship("Location")
    
    members = relationship("User", secondary=event_members_association)
    
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category")
    

    def __init__(self, topic, text, language_level, date, max_members, current_num_members, created, updated):
        self.topic = topic
        self.language_level = language_level
        # self.event_author = event_author
        self.text = text
        self.date = date
        self.max_members = max_members
        self.current_num_members = current_num_members
        self.created = created
        self.updated = updated
