import ujson
import falcon

from .constants import Status
from .helpers import row2dict
from db import models


class Ping:
    def on_get(self, request, response):
        response.set_header('Content-Type', 'application/json')
        response.status = falcon.HTTP_200
        response.body = ujson.dumps({'status': Status.OK})


class Items:
    model = None

    def on_get(self, request, response):
        session = request.context['session']
        items = session.query(self.model).all()

        response.set_header('Content-Type', 'application/json')
        response.status = falcon.HTTP_200
        response.body = ujson.dumps(
            {
                'status': Status.OK,
                'data': [row2dict(item) for item in items]
            }
        )


class Category(Items):
    model = models.Category


class Language(Items):
    model = models.Language
