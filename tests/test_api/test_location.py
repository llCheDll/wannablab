import falcon

from db.models import Country, Region, City, District
from api.constants import Status


def test_districts(session, client):
    districts = []

    country = Country(id=1, title='Ukraine')
    region = Region(id=1, title='Kyivska region', country_id=1)
    city = City(id=1, title='Kyiv', region_id=1)

    for title in ['Obolonskiy', 'Pecherskiy']:
        districts.append(
            District(
                title=title,
                city_id=1
            )
        )

    session.add(country)
    session.add(region)
    session.add(city)
    session.add_all(districts)
    session.commit()

    resp = client.get('/api/v1/city/1/district/')
    error_resp = client.get('/api/v1/city/10/district/')

    assert resp.status == falcon.HTTP_OK
    assert resp.json['status'] == Status.OK
    assert error_resp.json['status'] == Status.NotFound

    for obj in resp.json['data']:
        assert obj['title'] in ['Obolonskiy', 'Pecherskiy']

    session.query(District).filter().delete()
    session.query(City).filter().delete()
    session.query(Region).filter().delete()
    session.query(Country).filter().delete()
    session.commit()


def test_cities(session, client):
    cities = []

    country1 = Country(id=1, title='Ukraine')
    country2 = Country(id=2, title='Poland')
    region1 = Region(id=1, title='Ivano-Frankivsk region', country_id=1)
    region2 = Region(id=2, title='Varshava region', country_id=1)

    cities.append(City(title='Ivano-Frankivsk', region_id=1))
    cities.append(City(title='Odessa', country_id=1))
    cities.append(City(title='Varshava', region_id=2))
    cities.append(City(title='Krakiv', country_id=2))

    session.add(country1)
    session.add(country2)
    session.add(region1)
    session.add(region2)
    session.add_all(cities)
    session.commit()

    resp_region = client.get('/api/v1/region/1/city/')
    resp_country = client.get('/api/v1/country/1/city/')
    error_resp = client.get('/api/v1/country/10/city/')

    assert resp_region.status == falcon.HTTP_OK
    assert resp_region.json['status'] == Status.OK
    assert resp_country.status == falcon.HTTP_OK
    assert resp_country.json['status'] == Status.OK
    assert error_resp.json['status'] == Status.NotFound

    for obj in resp_country.json['data']:
        assert obj['title'] in ['Odessa', 'Krakiv']

    for obj in resp_region.json['data']:
        assert obj['title'] in ['Ivano-Frankivsk', 'Varshava']

    session.query(City).filter().delete()
    session.query(Region).filter().delete()
    session.query(Country).filter().delete()
    session.commit()


def test_regions(session, client):
    regions = []

    country = Country(
        id=1,
        title='Ukraine',
    )

    for title in ['Ivano-Frankivsk', 'Kharkiv']:
        regions.append(
            Region(
                title=title,
                country_id=1
            )
        )

    session.add(country)
    session.add_all(regions)
    session.commit()

    resp = client.get('/api/v1/country/1/region/')
    error_resp = client.get('/api/v1/country/10/region/')

    assert resp.status == falcon.HTTP_OK
    assert resp.json['status'] == Status.OK
    assert error_resp.json['status'] == Status.NotFound

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

    resp = client.get('/api/v1/country/')

    assert resp.status == falcon.HTTP_OK
    assert resp.json['status'] == Status.OK

    for obj in resp.json['data']:
        assert obj['title'] in ['Ukraine', 'Poland']

    session.query(Country).filter().delete()
