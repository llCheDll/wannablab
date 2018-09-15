import pytest
from api.app import app as application
from db.utils import init_session


@pytest.fixture
def app():
    return application


_session = init_session()


@pytest.fixture
def session():
    return _session
