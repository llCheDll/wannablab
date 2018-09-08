import falcon
from .handlers import (
    Ping
)


def configure_app(application):
    application.add_route('/api/v1/ping/', Ping())

    return application


app = configure_app(falcon.API())
