import falcon

from db.models import Country, Region, City, District
from api.constants import Status


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


def test_region(session, client):
    regions = []

    for title in ['Ivano-Frankivsk', 'Kharkiv']:
        regions.append(
            Region(
                title=title
            )
        )
    session.add_all(regions)
    session.commit()

    resp = client.get('/api/v1/region/', as_response=True)

    assert resp.status == falcon.HTTP_OK
    assert resp.json['status'] == Status.OK

    for obj in resp.json['data']:
        assert obj['title'] in ['Ivano-Frankivsk', 'Kharkiv']

    session.query(Region).filter().delete()


def test_city(session, client):
    cities = []

    for title in ['Ivano-Frankivsk', 'Kharkiv']:
        cities.append(
            City(
                title=title
            )
        )
    session.add_all(cities)
    session.commit()

    resp = client.get('/api/v1/city/', as_response=True)

    assert resp.status == falcon.HTTP_OK
    assert resp.json['status'] == Status.OK

    for obj in resp.json['data']:
        assert obj['title'] in ['Ivano-Frankivsk', 'Kharkiv']

    session.query(City).filter().delete()


def test_district(session, client):
    districts = []

    for title in ['Dniprovskyi', 'Shevchenkivskyi']:
        districts.append(
            District(
                title=title
            )
        )
    session.add_all(districts)
    session.commit()

    resp = client.get('/api/v1/district/', as_response=True)

    assert resp.status == falcon.HTTP_OK
    assert resp.json['status'] == Status.OK

    for obj in resp.json['data']:
        assert obj['title'] in ['Dniprovskyi', 'Shevchenkivskyi']

    session.query(District).filter().delete()
