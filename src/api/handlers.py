import ujson
import falcon

from .constants import Status
from .helpers import row2dict
from db import models


class Ping:
    def on_get(self, req, resp):
        resp.set_header('Content-Type', 'application/json')
        resp.status = falcon.HTTP_200
        resp.body = ujson.dumps({'status': Status.OK})


class Category:
    def on_get(self, request, response):
        session = request.context['session']
        categories = session.query(models.Category).all()

        response.set_header('Content-Type', 'application/json')
        response.status = falcon.HTTP_200
        response.body = ujson.dumps({'status': Status.OK, 'data': [row2dict(cat) for cat in categories]})
