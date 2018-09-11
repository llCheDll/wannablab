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
    Numeric
)
from sqlalchemy_utils import EmailType


metadata = MetaData()
class_registry = {}


@as_declarative(class_registry=class_registry, metadata=metadata)
class Base:
    pass


user_language_association = Table('user_language', Base.metadata,
                                  Column('user_id', Integer, ForeignKey('user.id')),
                                  Column('language_id', Integer, ForeignKey('language.id'))
                                  )

friends_association_table = Table('friends', Base.metadata,
                                  Column('first_user', Integer, ForeignKey('user.id'), primary_key=True),
                                  Column('second_user', Integer, ForeignKey('user.id'), primary_key=True),
                                  UniqueConstraint('first_user', 'second_user', name='unique_friendships')
                                  )


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
    email = Column(EmailType, nullable=False, unique=True)
    facebook = Column(String, unique=True)
    instagram = Column(String, unique=True)
    twitter = Column(String, unique=True)
    password = Column(String, nullable=False)
    country = Column(String)
    city = Column(String)
    rating = Column(Integer)
    created = Column(Date, nullable=False)
    updated = Column(Date)
    deleted = Column(Boolean)

    language = relationship("Language", secondary=user_language_association)
    friends = relationship("User", secondary=friends_association_table,
                           primaryjoin=id == friends_association_table.c.first_user,
                           secondaryjoin=id == friends_association_table.c.second_user)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    created = Column(Date, nullable=False)
    updated = Column(Date)
    deleted = Column(Boolean)


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)

    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    author = relationship(
        "User",
        foreign_keys=[author_id],
        backref=backref("author_comments")
    )
    recipient = relationship(
        "User",
        foreign_keys=[recipient_id],
        backref=backref("recipient_comments")
    )

    text = Column(Text, nullable=False)
    created = Column(Date, nullable=False)
    updated = Column(Date)
    deleted = Column(Boolean)


event_members_association = Table(
    'event_members', Base.metadata,
    Column('event_id', Integer, ForeignKey('event.id')),
    Column('member_id', Integer, ForeignKey('user.id'))
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
    current_num_members = Column(Integer)

    created = Column(Date, nullable=False)
    updated = Column(Date)

    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship("Location")

    members = relationship("User", secondary=event_members_association)

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category")


class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    created = Column(Date, nullable=False)


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)

    latitude = Column(Numeric)
    longitude = Column(Numeric)

    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String)

    created = Column(Date, nullable=False)
    updated = Column(Date)


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
