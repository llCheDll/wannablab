import ujson
import falcon

from .constants import Status
from log.logger import Logger

class Ping:
    def on_get(self, req, resp):
        resp.set_header('Content-Type', 'application/json')
        resp.status = falcon.HTTP_200
        resp.body = ujson.dumps({'status': Status.OK})
        logger = Logger(f"{__name__}.ping")
        logger.info(resp.body)
