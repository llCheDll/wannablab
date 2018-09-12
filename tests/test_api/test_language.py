import falcon

from db.models import Language
from api.constants import Status


def test_languages(session, client):
    languages = []
    for title in ['English', 'Polish']:
        languages.append(
            Language(title=title, level=1)
        )
    session.add_all(languages)
    session.commit()

    resp = client.get('/api/v1/language/', as_response=True)

    assert resp.status == falcon.HTTP_OK
    assert resp.json['status'] == Status.OK

    for obj in resp.json['data']:
        assert obj['title'] in ['English', 'Polish']

    session.query(Language).filter().delete()
