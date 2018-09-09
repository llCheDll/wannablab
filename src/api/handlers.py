import ujson
import falcon

from .constants import Status
from .helpers import row2dict
from db import models


class Ping:
    def on_get(self, requset, response):
        response.set_header('Content-Type', 'application/json')
        response.status = falcon.HTTP_200
        response.body = ujson.dumps({'status': Status.OK})


class Category:
    def on_get(self, request, response):
        session = request.context['session']
        categories = session.query(models.Category).all()

        response.set_header('Content-Type', 'application/json')
        response.status = falcon.HTTP_200
        response.body = ujson.dumps(
            {
                'status': Status.OK,
                'data': [row2dict(cat) for cat in categories]
            }
        )


class Language:
    def on_get(self, request, response):
        session = request.context['session']
        languages = session.query(models.Language).all()

        response.set_header('Content-Type', 'application/json')
        response.status = falcon.HTTP_200
        response.body = ujson.dumps(
            {
                'status': Status.OK,
                'data': [row2dict(language) for language in languages]
            }
        )
