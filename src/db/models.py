from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    Text,
    Boolean,
    MetaData,
    Table,
    ForeignKey,
    UniqueConstraint,
    DateTime,
    Numeric,
    JSON,
    func
)


metadata = MetaData()
class_registry = {}


@as_declarative(class_registry=class_registry, metadata=metadata)
class Base:
    created = Column(DateTime, default=func.current_timestamp(), server_default=func.current_timestamp())
    updated = Column(DateTime, default=func.current_timestamp(), server_default=func.current_timestamp(),
                     onupdate=func.current_timestamp(), server_onupdate=func.current_timestamp())
    deleted = Column(Boolean, default=False)


user_language_association = Table(
    'user_language', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('language_id', Integer, ForeignKey('language.id'))
)


# friends_association_table = Table(
#     'friends', Base.metadata,
#     Column('first_user', Integer, ForeignKey('user.id'), primary_key=True),
#     Column('second_user', Integer, ForeignKey('user.id'), primary_key=True),
#     UniqueConstraint('first_user', 'second_user', name='unique_friendships')
# )


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    info = Column(Text)
    photo = Column(Integer)
    phone = Column(String)
    email = Column(String, nullable=False, unique=True)
    facebook = Column(String, unique=True)
    instagram = Column(String, unique=True)
    twitter = Column(String, unique=True)
    password = Column(String, nullable=False)
    country = Column(String)
    city = Column(String)
    rating = Column(Integer)

    language = relationship('Language', secondary=user_language_association)
    # friends = relationship('User', secondary=friends_association_table,
    #                        primaryjoin=id == friends_association_table.c.first_user,
    #                        secondaryjoin=id == friends_association_table.c.second_user)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)

    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    author = relationship(
        'User',
        foreign_keys=[author_id],
        backref=backref('author_comments')
    )
    recipient = relationship(
        'User',
        foreign_keys=[recipient_id],
        backref=backref('recipient_comments')
    )

    text = Column(Text, nullable=False)


event_members_association = Table(
    'event_members', Base.metadata,
    Column('event_id', Integer, ForeignKey('event.id')),
    Column('member_id', Integer, ForeignKey('user.id'))
)


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)

    author_id = Column(Integer, ForeignKey('user.id'))
    event_author = relationship('User')

    topic = Column(String)
    description = Column(Text)

    language_id = Column(Integer, ForeignKey('language.id'))
    language = relationship('Language')

    date = Column(DateTime, nullable=False)

    max_members = Column(Integer, nullable=False)
    current_num_members = Column(Integer)

    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship('Location')

    members = relationship('User', secondary=event_members_association)

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category')


class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    level = Column(Integer, nullable=False)


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    locations = relationship('Location')
    regions = relationship('Region')
    cities = relationship('City')


class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    country_id = Column(Integer, ForeignKey('country.id'))

    locations = relationship('Location')
    country = relationship('Country')
    cities = relationship('City')


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    region_id = Column(Integer, ForeignKey('region.id'))
    country_id = Column(Integer, ForeignKey('country.id'))

    locations = relationship('Location')
    region = relationship('Region')
    districts = relationship('District')


class District(Base):
    __tablename__ = 'district'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    city_id = Column(Integer, ForeignKey('city.id'))

    locations = relationship('Location')
    city = relationship('City')


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)

    latitude = Column(Numeric)
    longitude = Column(Numeric)

    address = Column(String, nullable=False)

    country_id = Column(Integer, ForeignKey('country.id'))
    region_id = Column(Integer, ForeignKey('region.id'))
    city_id = Column(Integer, ForeignKey('city.id'))
    district_id = Column(Integer, ForeignKey('district.id'))

    country = relationship('Country')
    region = relationship('Region')
    city = relationship('City')
    district = relationship('District')


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)

    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    author = relationship('User', foreign_keys=[author_id])
    recipient = relationship('User', foreign_keys=[recipient_id])

    text = Column(Text, nullable=False)

    received = Column(Boolean, nullable=False)


class Session(Base):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)
    session_id = Column(Integer)
    data = Column(JSON)
    expire = Column(DateTime)
