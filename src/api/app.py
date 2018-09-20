import falcon
from db.utils import init_session
from .handlers import (
    Event,
    Region,
    Country,
    City,
    District,
    Language,
    Category,
    Ping,
    MessageAll,
    MessageSent,
    MessageReceived,
    Message,
)
from .middlewares import DatabaseSessionManagerMiddleware


def configure_app(application):
    application.add_route('/api/v1/ping/', Ping())
    application.add_route('/api/v1/category/', Category())
    application.add_route('/api/v1/language/', Language())
    application.add_route('/api/v1/country/', Country())
    application.add_route('/api/v1/event/', Event())
    application.add_route('/api/v1/country/{country_id}/region/', Region())
    application.add_route('/api/v1/region/{region_id}/city/', City())
    application.add_route('/api/v1/country/{country_id}/city/', City())
    application.add_route('/api/v1/city/{city_id}/district/', District())
    application.add_route('/api/v1/user/{user_id}/message/all/', MessageAll())
    application.add_route('/api/v1/user/{user_id}/message/sent/', MessageSent())
    application.add_route(
        '/api/v1/user/{user_id}/message/received/',
        MessageReceived()
    )
    application.add_route(
        '/api/v1/message/{message_id}/',
        Message()
    )

    return application


session = init_session()
app = configure_app(falcon.API(middleware=[DatabaseSessionManagerMiddleware(session)]))
