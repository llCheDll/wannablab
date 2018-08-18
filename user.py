# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text, Unicode, orm, Boolean, Numeric
from sqlalchemy_utils import PhoneNumber, EmailType, CountryType

from base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String)
    birthday = Column(Date)
    info = Column(Text)
    photo = Column(Integer)
    language_level = Column(Integer)
    # phone = Column(PhoneNumberType(), nullable=False, unique=True)
    _phone_number = Column(Unicode(20))
    country_code = Column(Unicode(8))

    phonenumber = orm.composite(
        PhoneNumber,
        _phone_number,
        country_code
    )

    email = Column(EmailType)
    facebook = Column(String)
    instagram = Column(String)
    twitter = Column(String)
    password = Column(String, nullable=False)
    country = Column(CountryType)
    city = Column(String)
    rating = Column(Numeric)
    created = Column(Date)
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