import falcon
from datetime import date

from db.models import Message, User
from api.constants import Status


def test_message_all(session, client):
    session.query(Message).filter().delete()
    session.query(User).filter().delete()

    messages = []
    users = []
    texts = ['send text', 'received text']

    for i in range(1, 3):
        users.append(User(
            id=i,
            first_name=f'user{i}',
            last_name=f'user{i}',
            gender='male',
            birthday=date(2000, 1, 1),
            email=f'user{i}@gmail.com',
            password=f'user{i}',
        ))

    for i in range(1, 3):
        messages.append(Message(
            id=i,
            author_id=users[0].id,
            recipient_id=users[1].id,
            received=True,
            text=texts[0],
        ))
        messages.append(Message(
            id=i + 2,
            author_id=users[1].id,
            recipient_id=users[0].id,
            received=True,
            text=texts[1],
        ))

    session.add_all(users)
    session.add_all(messages)
    session.commit()

    resp_all = client.get('/api/v1/user/1/message/all/')
    resp_sent = client.get('/api/v1/user/1/message/sent/')
    resp_received = client.get('/api/v1/user/1/message/received/')
    resp_one = client.get('/api/v1/message/1/')
    error_resp = client.get('/api/v1/user/3/message/all/')

    assert resp_all.status == falcon.HTTP_OK
    assert resp_sent.status == falcon.HTTP_OK
    assert resp_received.status == falcon.HTTP_OK
    assert resp_one.status == falcon.HTTP_OK

    assert resp_all.json['status'] == Status.OK
    assert resp_sent.json['status'] == Status.OK
    assert resp_received.json['status'] == Status.OK
    assert resp_one.json['status'] == Status.OK
    assert error_resp.json['status'] == Status.NotFound

    for obj in resp_all.json['data']:
        assert obj['text'] in texts

    for obj in resp_sent.json['data']:
        assert obj['text'] == texts[0]

    for obj in resp_received.json['data']:
        assert obj['text'] == texts[1]

    resp_one.json['test'] = texts[1]

    session.query(Message).filter().delete()
    session.query(User).filter().delete()
    session.commit()
