import falcon
from db.utils import init_session
from .handlers import (
    Language,
    Category,
    Ping
)
from .middlewares import DatabaseSessionManagerMiddleware


def configure_app(application):
    application.add_route('/api/v1/ping/', Ping())
    application.add_route('/api/v1/category/', Category())
    application.add_route('/api/v1/language/', Language())

    return application


session = init_session()
app = configure_app(falcon.API(middleware=[DatabaseSessionManagerMiddleware(session)]))
