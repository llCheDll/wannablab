# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text, Unicode, orm, Boolean, Numeric, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PhoneNumber, EmailType, CountryType

from base import Base

user_language_association = Table('user_language', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('language_id', Integer, ForeignKey('language.id'))
)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    info = Column(Text)
    photo = Column(Integer)
    language = relationship("Language", secondary=user_language_association)
    language_level = Column(Integer) # FK M2M - ???
    phone = Column(String) # Column(PhoneNumberType(), nullable=False, unique=True)
    # _phone_number = Column(Unicode(20))
    # country_code = Column(Unicode(8))

    # phonenumber = orm.composite(
    #     PhoneNumber,
    #     _phone_number,
    #     country_code
    # )

    email = Column(EmailType, nullable=False, unique=True)
    facebook = Column(String, unique=True)
    instagram = Column(String, unique=True)
    twitter = Column(String, unique=True)
    password = Column(String, nullable=False)
    country = Column(String)# CountryType, nullable=False)
    city = Column(String)
    rating = Column(Integer)# Numeric)
    comments = relationship("Comment")
    created = Column(Date, nullable=False)
    updated = Column(Date)
    deleted = Column(Boolean)

    def __init__(self, name, gender, birthday, info, photo, language_level, phone, email, facebook, instagram, twitter,
        password, country, city, rating, created, updated, deleted):
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.info = info
        self.photo = photo
        self.language_level = language_level
        self.phone = phone
        self.email = email
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter
        self.password = password
        self.country = country
        self.city = city
        self.rating = rating
        self.created = created
        self.updated = updated
        self.deleted = deleted