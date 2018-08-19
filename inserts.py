# coding=utf-8

# imports
from datetime import date

from sqlalchemy import func

from base import Session, engine, Base
from category import Category
from comment import Comment
from event import Event
from user import User
from language import Language
from message import Message
from location import Location

# generate database schema
Base.metadata.create_all(engine)

# create a new session
session = Session()

# creates entities
for x in range(500):
    i = x

    user = 'user_' + str(x)
    event = 'event_' + str(x)
    language = 'language_' + str(x)
    comment = 'comment_' + str(x)
    category = 'category_' + str(x)
    message = 'message_' + str(x)
    location = 'location_' + str(x)

    receiver = 'receiver_' + str(x)

    location = Location(x, x+1, x, x, x, date(2002, 10, 11), date(2002, 10, 11), False)
    language = Language(language, 2, date(2002, 10, 11))
    category = Category(category, date(2002, 10, 11), date(2002, 10, 12), False)
    user = User(user, "Man", date(2002, 10, 11), "some text...", 42, 5, "3067", user, user, user, user,
        "password", "us", "Denver", 4, date(2018, 10, 11), date(2002, 10, 11), False)
    event =  Event(event, "some text...", 3, date(2002, 10, 11), 5, 3, date(2002, 10, 11), date(2002, 10, 11))
    comment = Comment(comment, date(2002, 10, 11), date(2002, 10, 12), False)
    message = Message(message, date(2002, 10, 11), True, date(2002, 10, 11), False)

    receiver = User(receiver, "Girl", date(2002, 10, 11), "some text...", 42, 5, "3067", user, user, user, user,
        "password", "us", "Denver", 4, date(2018, 10, 11), date(2002, 10, 11), False)

# add members to events
    event.members = [user, user, user, user]

# add category to event
    event.category = category

# add language to event
    event.language = language

# add author to event
    event.event_author = user

# add receiver to message
    message.receiver = receiver

# persists data
    session.add(event)
    session.add(user)
    session.add(language)
    session.add(comment)
    session.add(message)
    session.add(location)

# commit and close session
session.commit()
session.close()