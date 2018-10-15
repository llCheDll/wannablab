from datetime import date
import falcon

from db.models import User, Language
from api.constants import Status


def test_user_profile(session, client):
    users = session.query(User).filter()

    for user in users:
        user.friends.clear()
        user.language.clear()

    session.query(User).filter().delete()
    session.query(Language).filter().delete()

    users = []
    language = Language(
        id=1,
        title='english',
        level=1,
    )
    session.add(language)

    for i in range(1, 4):
        users.append(User(
            id=i,
            first_name=f'user{i}',
            last_name=f'user{i}',
            gender='male',
            birthday=date(2000, 1, 1),
            info='info1',
            email=f'user{i}@gmail.com',
            password=f'user{i}',
            language=[language],
        ))
    users[0].friends = [users[1], users[2]]

    session.add_all(users)
    session.commit()

    resp_exist = client.get('/api/v1/user/1/')
    resp_not_exist = client.get('/api/v1/user/4/')

    assert resp_exist.status == falcon.HTTP_OK
    assert resp_not_exist.status == falcon.HTTP_404
    assert resp_exist.json['status'] == Status.OK
    assert resp_not_exist.json['status'] == Status.NotFound

    for user in users:
        user.friends.clear()
        user.language.clear()
    session.query(User).filter().delete()
    session.query(Language).filter().delete()
    session.commit()
