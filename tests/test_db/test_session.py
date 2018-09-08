from db.utils import init_session


def test_session():
    session = init_session()
    res = session.execute('SELECT * FROM pg_stat_activity LIMIT 1')

    assert len(res.fetchall()) > 0
