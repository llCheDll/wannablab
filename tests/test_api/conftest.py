import pytest
from api.app import app as application


@pytest.fixture
def app():
    return application
