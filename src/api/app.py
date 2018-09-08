import ujson
import falcon


class Ping(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = ujson.dumps({'status': 'ok'})


api = application = falcon.API()
api.add_route('/api/v1/ping/', Ping())