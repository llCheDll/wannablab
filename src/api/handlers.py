import ujson
import falcon

from .constants import Status


class Ping(object):
    def on_get(self, req, resp):
        resp.set_header('Content-Type', 'application/json')
        resp.status = falcon.HTTP_200
        resp.body = ujson.dumps({'status': Status.OK})
