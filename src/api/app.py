import falcon
from db.utils import init_session
from .handlers import (
    Region,
    Country,
    City,
    District,
    Language,
    Category,
    Ping
)
from .middlewares import DatabaseSessionManagerMiddleware


def configure_app(application):
    application.add_route('/api/v1/ping/', Ping())
    application.add_route('/api/v1/category/', Category())
    application.add_route('/api/v1/language/', Language())
    application.add_route('/api/v1/country/', Country())
    application.add_route('/api/v1/{country_id}/region/', Region())
    application.add_route('/api/v1/{country_id}/city/', City())
    # application.add_route('/api/v1/{city_id}/district/', District())

    return application


session = init_session()
app = configure_app(falcon.API(middleware=[DatabaseSessionManagerMiddleware(session)]))
