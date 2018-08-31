from base import Session

from category import Category
from event import Event
from language import Language
from location import Location
from user import User

session = Session()

filtered_events_list = session.query(Event).join(
	User, Event.author_id == User.id).join(Location,
	Event.location_id == Location.id).join(
	Category, Event.category_id == Category.id).join(
	Language, Event.language_id == Language.id).filter(
    User.city == 'Kyiv',
    Event.max_members == 5,
    Location.country == 'Ukraine',
    # Category.title == 'category_26'
    # Language.title == 'language_64'
    # Location.address == 'вул.Верхній Вал 21'
).all()

print('List of events with filters:')
for event in filtered_events_list[:5]:
    print(event)

session.close()