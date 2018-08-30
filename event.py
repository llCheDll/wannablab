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
    

    def __init__(self,
                 author_id,
                 topic,
                 description,
                 language_id,
                 date,
                 max_members,
                 created,
                 location_id,
                 category_id):
        self.author_id = author_id
        self.topic = topic
        self.description = description
        self.language_id = language_id
        self.date = date
        self.max_members = max_members
        self.current_num_members = 1
        self.created = created
        self.updated = None
        self.location_id = location_id
        self.category_id = category_id
