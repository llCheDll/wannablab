USERS_QTY = 500
EVENTS_QTY = 50
LANGUAGES_QTY = 150
LANGUAGE_LVL_QTY = 5
CATEGORIES_QTY = 30
MAX_MEMBERS_QTY = 6
MAX_RATING = 300

from datetime import date
from random import randint

from base import Session, engine, Base
from category import Category
from comment import Comment
from event import Event
from user import User
from language import Language
from message import Message
from location import Location

# generate database schema
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# create a new session
session = Session()

# create languages
for i in range(LANGUAGES_QTY):
    language_name = "language_" + str(i)

    for language_level in range(LANGUAGE_LVL_QTY):
        language = Language(
            language_name,
            language_level,
            date(2002, 10, 11)
        )
        session.add(language)

session.commit()

# create categories
for i in range(CATEGORIES_QTY):
    category_name = "category_" + str(i)
    category = Category(
        category_name,
        date(2002, 10, 11)
    )
    session.add(category)

session.commit()

# create users
for i in range(USERS_QTY):
    user_name = 'user_' + str(i+1)
    language_id = [
        session.query(Language).get(
            randint(1, LANGUAGES_QTY * LANGUAGE_LVL_QTY)
        ),
        session.query(Language).get(
            randint(1, LANGUAGES_QTY * LANGUAGE_LVL_QTY)
        ),
        session.query(Language).get(
            randint(1, LANGUAGES_QTY * LANGUAGE_LVL_QTY)
        ),
    ]
    rating = randint(0, MAX_RATING)

    user = User(
        user_name,
        user_name,
        'male',
        date(2000, 1, 1),
        f'Very long info string of {user_name}',
        language_id,
        str(randint(100000000000, 1000000000000)),
        f'{user_name}@gmail.com',
        f'facebook_{user_name}',
        f'instagram_{user_name}',
        f'twitter_{user_name}',
        user_name,
        'Ukraine',
        "Kyiv",
        rating,
        date(2002, 10, 11)
    )
    session.add(user)

session.commit()

# create locations
for i in range(EVENTS_QTY):
    location = Location(
        50.470040,
        30.518723,
        'Ukraine',
        'Kyiv',
        f'вул.Верхній Вал {i+1}',
        date(2002, 10 ,11)
    )
    session.add(location)

session.commit()

# create events
for i in range(EVENTS_QTY):
    author_id = randint(1, USERS_QTY)
    language_id = randint(1, LANGUAGES_QTY * LANGUAGE_LVL_QTY)
    max_members = randint(2, MAX_MEMBERS_QTY)
    current_id = i + 1
    category_id = randint(1, CATEGORIES_QTY)

    event = Event(
        author_id,
        f'Topic of event {current_id}.',
        f'Very long description of event {current_id}',
        language_id,
        date(2018, 10, 1),
        max_members,
        date(2018, 1, 1),
        current_id,
        category_id
    )
    session.add(event)

session.commit()

# add members to events
for i in range(EVENTS_QTY):
    current_event = session.query(Event).get(i+1)

    members = []
    for j in range(current_event.max_members-1):
        members.append(
            session.query(User).get(randint(1, USERS_QTY))
        )
    current_event.members = members
    session.add(current_event)

session.commit()

# close session
session.close()
