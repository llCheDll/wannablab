import falcon
from api.constants import Status


def test_ping(client):
    resp = client.get('/api/v1/ping', as_response=True)

    assert resp.status == falcon.HTTP_OK
    assert resp.json['status'] == Status.OK
