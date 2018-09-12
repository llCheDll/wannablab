import falcon

from db.models import Country, Region, City
from api.constants import Status


def test_city(session, client):
    cities = []

    country = Country(
        id=2,
        title='Ukraine',
    )

    region = Region(
        id=2,
        title='Ivano-Frankivsk region',
        country_id=2
    )
    for title in ['Ivano-Frankivsk', 'Kharkiv']:
        cities.append(
            City(
                title=title,
                region_id=2
            )
        )

    session.add(country)
    session.add(region)
    session.add_all(cities)
    session.commit()

    resp = client.get('/api/v1/2/city/', as_response=True)

    assert resp.status == falcon.HTTP_OK
    assert resp.json['status'] == Status.OK

    for obj in resp.json['data']:
        assert obj['title'] in ['Ivano-Frankivsk', 'Kharkiv']

    session.query(City).filter().delete()
    session.query(Region).filter().delete()
    session.query(Country).filter().delete()
    session.commit()


def test_region(session, client):
    regions = []

    country = Country(
        id=2,
        title='Ukraine',
    )

    for title in ['Ivano-Frankivsk', 'Kharkiv']:
        regions.append(
            Region(
                title=title,
                country_id=2
            )
        )

    session.add(country)
    session.add_all(regions)
    session.commit()

    resp = client.get('/api/v1/2/region/', as_response=True)

    assert resp.status == falcon.HTTP_OK
    assert resp.json['status'] == Status.OK

    for obj in resp.json['data']:
        assert obj['title'] in ['Ivano-Frankivsk', 'Kharkiv']

    session.query(Region).filter().delete()
    session.query(Country).filter().delete()
    session.commit()


def test_countries(session, client):
    countries = []

    for title in ['Ukraine', 'Poland']:
        countries.append(
            Country(
                title=title
            )
        )
    session.add_all(countries)
    session.commit()

    resp = client.get('/api/v1/country/', as_response=True)

    assert resp.status == falcon.HTTP_OK
    assert resp.json['status'] == Status.OK

    for obj in resp.json['data']:
        assert obj['title'] in ['Ukraine', 'Poland']

    session.query(Country).filter().delete()
