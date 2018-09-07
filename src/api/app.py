import json
import falcon


class Ping(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps('pong!')


api = application = falcon.API()
api.add_route('/', Ping())