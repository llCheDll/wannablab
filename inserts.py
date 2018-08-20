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

    user_name = 'user_' + str(x)
    event_name = 'event_' + str(x)
    language_name = 'language_' + str(x)
    comment_name = 'comment_' + str(x)
    category_name = 'category_' + str(x)
    message_name = 'message_' + str(x)
    location_name = 'location_' + str(x)
    recipient_name = 'recipient_' + str(x)

    location = Location(x, x+1, x, x, x, date(2002, 10, 11), date(2002, 10, 11), False)
    language = Language(language_name, 2, date(2002, 10, 11))
    category = Category(category_name, date(2002, 10, 11), date(2002, 10, 12), False)

    user = User(user_name, "Man", date(2002, 10, 11), "some text...", 42, 5, "3067", user_name, user_name, user_name, user_name,
        "password", "us", "Denver", 4, date(2018, 10, 11), date(2002, 10, 11), False)

    event =  Event(event_name, "some text...", 3, date(2002, 10, 11), 5, 3, date(2002, 10, 11), date(2002, 10, 11))

    recipient = User(recipient_name, "Man", date(2002, 10, 11), "some text...", 42, 5, "3067", recipient_name, recipient_name, recipient_name, recipient_name,
        "password", "us", "Denver", 4, date(2018, 10, 11), date(2002, 10, 11), False)
    
    session.add(user)
    session.add(recipient)
    session.commit()
    
    comment = Comment(user.id, recipient.id, comment_name, date(2002, 10, 11), date(2002, 10, 12), False)
    
    message = Message(message_name, date(2002, 10, 11), user.id, recipient.id, True, date(2002, 10, 11), False)

# add members to events
    event.members = [user, user, user, user]

# add category to event
    event.category = category

# add language to event
    event.language = language

# add author to event
    event.event_author = user

# persists data
    session.add(event)
    session.add(language)
    session.add(comment)
    session.add(message)
    session.add(location)

# commit and close session
session.commit()
session.close()
