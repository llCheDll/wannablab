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
from message import Message

# 2 - extract a session
session = Session()

# 3 - extract all events
events = session.query(Event).all()
users = session.query(User).all()
messages = session.query(Message).all()

# 4 - print events' details
# print('\n### All events:')
# for event in events:
    # print(f'{event.event_author.id}')
    # print(f'{event.topic} was released on {event.created} {event.topic}')
#     print('event members: ')
#     for member in event.members:
#         print(f'{member.name}')
# print('')
# 5 - print users' details
# print('\n### All users:')
# for user in users:
#     print(f'{user.id}')
# print('')

# print messages
print('\n### All messages:')
for message in messages:
    print(f'message_id: {message.id}')
    print(f'author_id: {message.author_id}')
    print(f'message_recepient: {message.recipient_id}')
    print(f'text: {message.text}')
    print(f'created: {message.created}')
    print(f'updated: {message.updated}')
    print(f'deleted: {message.deleted}')
print('')
