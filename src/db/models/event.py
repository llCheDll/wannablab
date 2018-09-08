# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, Text, DateTime
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

    date = Column(DateTime, nullable=False)

    max_members = Column(Integer, nullable=False)
    current_num_members = Column(Integer)  # ???

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

    def __str__(self):
        event_string = (
            f'event_id: \t{self.id}\n'

            f'author_id {self.event_author.id}: \t'
            f'{self.event_author.first_name} {self.event_author.last_name}\n'

            f'topic: \t{self.topic}\n'
            f'description: \t{self.description}\n'
            f'date: \t{self.date}\n'
            f'max_members: \t\t{self.max_members}\n'
            f'current_num_members: \t\t{self.current_num_members}\n'

            f'language_id {self.language.id}: \t'
            f'{self.language.title}(level_{self.language.level})\n'

            f'category_id {self.category.id}: \t {self.category.title}\n'
            f'location_id {self.location.id}: \t {self.location.address}\n'
            f'Members:\n'
        )

        for i in self.members:
            event_string += f'member_id {i.id}: \t {i.first_name} {i.last_name}\n'

        event_string += (
            f'created: \t{self.created}\n'
            f'updated: \t{self.updated}\n'
        )

        return event_string

