from base import Session

from category import Category
from comment import Comment
from event import Event
from language import Language
from location import Location
from message import Message
from user import User

session = Session()

# extract users list without filter
# users_list = session.query(User).all()
# print('List of users without filters selected:')
# for user in users_list[:5]:
#     print(user)


filtered_users_list = session.query(User).join(Language, User.language).filter(
    User.city == 'Kyiv',
    Language.title == 'language_2'
)
print('List of users with filters selected:')
for user in filtered_users_list[:4]:
    print(user)


# import ipdb
# ipdb.set_trace()

session.close()
