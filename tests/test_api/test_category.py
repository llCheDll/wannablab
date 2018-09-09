import falcon

from db.models import Category
from datetime import date
from api.constants import Status


def test_categories(session, client):
    categories = []
    for title in ['sport', 'music']:
        categories.append(
            Category(title=title, created=date(year=2018, month=9, day=1), deleted=False)
        )
    session.add_all(categories)
    session.commit()

    resp = client.get('/api/v1/category/')

    assert resp.status == falcon.HTTP_OK
    assert resp.json['status'] == Status.OK

    for obj in resp.json['data']:
        assert obj['title'] in ['sport', 'music']

    session.query(Category).filter().delete()
