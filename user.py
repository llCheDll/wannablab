# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, Text, Unicode, orm, Boolean, Numeric, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PhoneNumber, EmailType, CountryType

# from passlib.hash import bcrypt

from base import Base

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
    
    language = relationship("Language", secondary=user_language_association)
    # language_level = Column(Integer)  FK M2M - ???
    
    # _phone_number = Column(Unicode(20))
    # country_code = Column(Unicode(8))

    # phonenumber = orm.composite(
    #     PhoneNumber,
    #     _phone_number,
    #     country_code
    # )
    # messages = relationship("Message")

    phone = Column(String) # Column(PhoneNumberType(), nullable=False, unique=True)
    email = Column(EmailType, nullable=False, unique=True)
    facebook = Column(String, unique=True)
    instagram = Column(String, unique=True)
    twitter = Column(String, unique=True)
    password = Column(String, nullable=False)
    country = Column(String)# CountryType, nullable=False)
    city = Column(String)
    rating = Column(Integer)# Numeric)

    #_ratings = Column(db.String, default='0.0')
    #
    # @property
    # def ratings(self):
    #     return [float(x) for x in self._ratings.split(';')]
    
    # @ratings.setter
    # def ratings(self, value):
    #     self._ratings += ';%s' % value
    
    created = Column(Date, nullable=False)
    updated = Column(Date)
    deleted = Column(Boolean)
    
    friends = relationship("User", secondary=friends_association_table, 
        primaryjoin=id==friends_association_table.c.first_user,
        secondaryjoin=id==friends_association_table.c.second_user)

    def __init__(self,
                 first_name,
                 last_name,
                 gender,
                 birthday,
                 info,
                 # photo,
                 language_id,
                 phone,
                 email,
                 facebook,
                 instagram,
                 twitter,
                 password,
                 country,
                 city,
                 rating,
                 created):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birthday = birthday
        self.info = info
        # self.photo = photo
        self.language = language_id
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
        self.updated = None
        self.deleted = False

    def __str__(self):
        user_string = (
            f'user_id: \t{self.id}\n'
            f'first_name: \t{self.first_name}\n'
            f'last_name: \t{self.last_name}\n'
            f'gender: \t{self.gender}\n'
            f'birthday: \t{self.birthday}\n'
            f'info: \t\t{self.info}\n'
        )

        for i in self.language:
            user_string += f'language_id {i.id}: \t {i.title}(level_{i.level})\n'

        user_string += (
            f'phone: \t\t{self.phone}\n'
            f'email: \t{self.email}\n'   
            f'facebook: \t{self.facebook}\n'
            f'instagram: \t{self.instagram}\n'
            f'twitter: \t{self.twitter}\n'
            f'password: \t{self.password}\n'
            f'country: \t{self.country}\n'
            f'city: \t\t{self.city}\n'
            f'rating: \t{self.rating}\n'
            f'created: \t{self.created}\n'
            f'updated: \t{self.updated}\n'
            f'deleted: \t{self.deleted}\n'
        )
        return user_string 
           
    # def validate_password(self, password):
    #     return bcrypt.verify(password, self.password)
