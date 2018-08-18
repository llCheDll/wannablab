# coding=utf-8

# 1 - imports
from datetime import date

from base import Session, engine, Base
from category import Category
from comment import Comment
from event import Event
from user import User
from language import Language
from location import Location

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

# 4 - create users
john = User("John Snow", "Man", date(2002, 10, 11), "some text...", 42, 3, "3067", "john1.snow@zalupa.com",
    "facebook.john1.snow", "instagram.john1.snow", "twitter.john1.snow",
        "password", "us", "Denver", 4, date(2018, 10, 11), date(2002, 10, 11), False)
# smith = User("Smith Snow", "M", date(2002, 10, 11), "some text...", 42, 3, "3067", "smith.snow@zalupa.com",
#     "facebook.smith.snow", "instagram.smith.snow", "twitter.smith.snow",
#         "password", "USA", "Denver", 4, date(2018, 10, 11), date(2002, 10, 11), False)
# alex = User("Alex Snow", "M", date(2002, 10, 11), "some text...", 42, 3, "3067", "alex.snow@zalupa.com",
#     "facebook.alex.snow", "instagram.alex.snow", "twitter.alex.snow",
#         "password", "USA", "Denver", 4, date(2018, 10, 11), date(2002, 10, 11), False)

# 5 - creates events
some_event_1 = Event("Sport talking", 3, "John", date(2002, 10, 11), 5, 3, date(2002, 10, 11), date(2002, 10, 11))
some_event_2 = Event("Sport talking", 3, "smith", date(2002, 10, 11), 5, 3, date(2002, 10, 11), date(2002, 10, 11))
some_event_3 = Event("Sport talking", 3, "alex", date(2002, 10, 11), 5, 3, date(2002, 10, 11), date(2002, 10, 11))

# 6 - add members to events
some_event_1.members = [john]
# some_event_2.members = [smith]
# some_event_3.members = [alex, smith]

# 7 - add contact details to actors
# matt_contact = ContactDetails("415 555 2671", "Burbank, CA", matt_damon)
# dwayne_contact = ContactDetails("423 555 5623", "Glendale, CA", dwayne_johnson)
# dwayne_contact_2 = ContactDetails("421 444 2323", "West Hollywood, CA", dwayne_johnson)
# mark_contact = ContactDetails("421 333 9428", "Glendale, CA", mark_wahlberg)

# 8 - create stuntmen
# matt_stuntman = Stuntman("John Doe", True, matt_damon)
# dwayne_stuntman = Stuntman("John Roe", True, dwayne_johnson)
# mark_stuntman = Stuntman("Richard Roe", True, mark_wahlberg)

# 9 - persists data
session.add(some_event_1)
# session.add(some_event_2)
# session.add(some_event_3)
session.add(john)
# session.add(smith)
# session.add(alex)

# session.add(matt_contact)
# session.add(dwayne_contact)
# session.add(dwayne_contact_2)
# session.add(mark_contact)

# session.add(matt_stuntman)
# session.add(dwayne_stuntman)
# session.add(mark_stuntman)

# 10 - commit and close session
session.commit()
session.close()