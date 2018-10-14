from datetime import date, datetime
from random import randint
from invoke import task
from base import Session, engine, Base

from db.models import (
    Category,
    Comment,
    Event,
    User,
    Language,
    Message,
    Location,
    Country,
    Region,
    City,
    District
)

USERS_QTY = 10
EVENTS_QTY = 10
LANGUAGES_QTY = 10
LANGUAGE_LVL_QTY = 5
CATEGORIES_QTY = 10
MAX_MEMBERS_QTY = 6
MAX_FRIENDS_QTY = 2
MAX_RATING = 100
cities = []


@task(
    help={
        "db": "Database name, default: master."
    }
)
def insert(ctx):
    """
       Insert values to db.
     """

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
                title=language_name,
                level=language_level,
            )
            session.add(language)

    session.commit()

    # create categories
    for i in range(CATEGORIES_QTY):
        category_name = "category_" + str(i)
        category = Category(
            title=category_name,
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
            first_name=user_name,
            last_name=user_name,
            gender='male',
            info=f'Very long info string of {user_name}',
            password=str(randint(100000000000, 1000000000000)),
            email=f'{user_name}@gmail.com',
            facebook=f'facebook_{user_name}',
            instagram=f'instagram_{user_name}',
            twitter=f'twitter_{user_name}',
            country='Ukraine',
            city="Kyiv",
            rating=rating,
            birthday=date(2002, 10, 11),
            language=language_id,
        )
        session.add(user)

    session.commit()

    for i in range(EVENTS_QTY):
        country = Country(
            title=f'country_{i}'
        )
        session.add(country)

        region = Region(
            title=f'region_{i}',
            country_id=i+1
        )
        session.add(region)

        cities.append(City(title=f'city_by_country_{i+1}', country_id=i + 1))
        cities.append(City(title=f'city_by_region_{i+1}', region_id=i + 1))
        session.add_all(cities)

        district = District(
            title=f'district_{i}',
            city_id=i+1
        )
        session.add(district)

    session.commit()

    # create locations
    for i in range(EVENTS_QTY):
        location = Location(
            latitude=50.470040,
            longitude=30.518723,
            country_id=i+1,
            region_id=i+1,
            city_id=i+1,
            district_id=i+1,
            address=f'вул.Верхній Вал {i+1}'
        )
        session.add(location)

    session.commit()

    # create events
    for i in range(EVENTS_QTY):
        author_id = randint(1, USERS_QTY)
        location_id = randint(1, EVENTS_QTY)
        language_id = randint(1, LANGUAGES_QTY * LANGUAGE_LVL_QTY)
        max_members = randint(2, MAX_MEMBERS_QTY)
        current_id = i + 1
        category_id = randint(1, CATEGORIES_QTY)

        event = Event(
            author_id=author_id,
            topic=f'Topic of event {current_id}.',
            description=f'Very long description of event {current_id}',
            language_id=language_id,
            date=datetime(2018, 10, 1, 19, 00, 00),
            max_members=max_members,
            current_num_members=2,
            category_id=category_id,
            location_id=location_id
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

    # add friends
    for i in range(1, USERS_QTY-MAX_FRIENDS_QTY, MAX_FRIENDS_QTY+1):
        current_user = session.query(User).get(i)

        friends = []
        for j in range(1, MAX_FRIENDS_QTY+1):
            friends.append(
                session.query(User).get(i+j)
            )
        current_user.friends = friends
        session.add(current_user)

    # create messages
    for i in range(USERS_QTY):
        message = Message(
            text=f"Message text with id: {i+1}",
            id=i+1,
            author_id=randint(1, USERS_QTY),
            recipient_id=randint(1, USERS_QTY),
            received=True
        )
        session.add(message)

    session.commit()

    # create comments
    for i in range(USERS_QTY):
        comment = Comment(
            id=i + 1,
            author_id=randint(1, USERS_QTY),
            text=f"Comment text with id: {i+1}",
            recipient_id=randint(1, USERS_QTY)

        )
        session.add(comment)

    session.commit()

    # close session
    session.close()
