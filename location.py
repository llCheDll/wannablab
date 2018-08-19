# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from base import Base


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)

    latitude = Column(Numeric)
    longitude = Column(Numeric)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String)
    event_id = Column(Integer, ForeignKey('event.id'))
    event = relationship("Event")
    created = Column(Date, nullable=False)
    updated = Column(Date)

    def __init__(self, latitude, longitude, text, created, received, updated, deleted):
        self.latitude = latitude
        self.longitude = longitude
        self.text = text
        self.created = created
        self.received = received
        self.updated = updated
        self.deleted = deleted