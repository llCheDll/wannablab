from datetime import date
import falcon

from db.models import Event, User, Language, Country, Region, City, District, Location, Category
from api.constants import Status


def test_event(session, client):

    events = []

    languages = []
    for title in ['English', 'Polish']:
        languages.append(
            Language(title=title, level=1)
        )
    session.add_all(languages)

    country = Country(title='Ukraine')
    region = Region(title='Kyivska region', country=country)
    city = City(title='Kyiv', region=region)
    district = District(title='Obolonskiy', city=city)

    session.add(country)
    session.add(region)
    session.add(city)
    session.add(district)

    category = Category(title="sport")
    location = Location(address="adress", country=country, region=region, city=city, district=district)

    session.add(location)
    session.add(category)

    member = User(
        id=15,
        first_name='name',
        last_name='last_name',
        gender='male',
        birthday=date(2000, 1, 1),
        info='info',
        email='user2@gmail.com',
        password='user_password',

    )
    session.add(member)

    for i in range(17, 18):
        events.append(Event(
            id=i,
            event_author=member,
            topic="Topic",
            description="description",
            language=languages[0],
            date=date(2000, 1, 1),
            max_members=4,
            current_num_members=1,
            location=location,
            members=[member],
            category=category
        ))

    session.add_all(events)
    session.commit()

    resp_exist = client.get('/api/v1/event/17/')
    resp_not_exist = client.get('/api/v1/event/19/')

    assert resp_exist.status == falcon.HTTP_OK
    assert resp_not_exist.status == falcon.HTTP_404
    assert resp_exist.json['status'] == Status.OK
    assert resp_not_exist.json['status'] == Status.NotFound

    session.commit()
