import falcon
from sqlalchemy import or_
import ujson

from .constants import Status
from .helpers import row2dict, load_template, parse_data
from db import models


class Ping:
    def on_get(self, request, response):
        response.set_header('Content-Type', 'application/json')
        response.status = falcon.HTTP_200
        response.body = ujson.dumps({'status': Status.OK})


class Logout:
    def on_get(self, request, response):
        template = load_template('logout.html')
        response.status = falcon.HTTP_200
        response.content_type = 'text/html'
        response.body = template.render(something='testing')

    def on_post(self, request, response):
        body = request.stream.read()

        if isinstance(body, bytes):
            body = body.decode()

        body = falcon.uri.parse_query_string(body)

        if body['accept']:
            response.unset_cookie('token')
            response.body = ujson.dumps({"message": "You logout succesfuly"})
            response.status = falcon.HTTP_201


class Login:
    def on_post(self, request, response):
        body = request.stream.read()

        if isinstance(body, bytes):
            body = body.decode()

        body = falcon.uri.parse_query_string(body)

        model = models.User
        session = request.context['session']
        user = session.query(model).filter(
                model.first_name==body['uname']
                        ).filter(
                    model.password==body['psw']).all()

        if not user:
            response.body = ujson.dumps({"message": "Your login or password incorrect"})
            response.status = falcon.HTTP_401
        else:
            response.set_cookie(name='token', value='jkhaslkjdf', path='/api/v1/', secure=False)
            response.body = ujson.dumps({"message": "You Log In"})
            response.status = falcon.HTTP_200

    def on_get(self, request, response):
        template = load_template('login.html')
        response.status = falcon.HTTP_200
        response.content_type = 'text/html'
        response.body = template.render(something='testing')


class Register:
    pass


class Items:
    model = None

    def on_get(self, request, response, **kwargs):
        # import ipdb
        # ipdb.set_trace()
        session = request.context['session']
        items = self._get_items(session, self.model, **kwargs)
        data_list = [row2dict(item) for item in items]

        if data_list:
            response.status = falcon.HTTP_200
            body = {
                'status': Status.OK,
                'data': data_list
            }
        else:
            response.status = falcon.HTTP_404
            body = {
                'status': Status.NotFound,
            }

        response.set_header('Content-Type', 'application/json')
        response.body = ujson.dumps(body)

    def _get_items(self, session, model, **kwargs):
        return session.query(model).all()


class Category(Items):
    model = models.Category


class Language(Items):
    model = models.Language


class Country(Items):
    model = models.Country


class Region(Items):
    model = models.Region

    def _get_items(self, session, model, **kwargs):
        country_id = kwargs.get('country_id')
        regions = session.query(model).filter(model.country_id == country_id).all()
        return regions


class City(Items):
    model = models.City

    def _get_items(self, session, model, **kwargs):
        country_id = kwargs.get('country_id')
        region_id = kwargs.get('region_id')
        cities = session.query(models.City).filter(
            model.country_id == country_id
        ).filter(
            model.region_id == region_id
        )
        return cities


class District(Items):
    model = models.District

    def _get_items(self, session, model, **kwargs):
        city_id = kwargs.get('city_id')
        districts = session.query(model).filter(
            model.city_id == city_id
        ).all()
        return districts


class MessageAll(Items):
    model = models.Message

    def _get_items(self, session, model, **kwargs):
        items = session.query(model).filter(or_(
            model.author_id == kwargs['user_id'],
            model.recipient_id == kwargs['user_id'],
        )).all()

        return items


class MessageSent(Items):
    model = models.Message

    def _get_items(self, session, model, **kwargs):
        items = session.query(model).filter(
            model.author_id == kwargs['user_id'],
        ).all()

        return items


class MessageReceived(Items):
    model = models.Message

    def _get_items(self, session, model, **kwargs):
        items = session.query(model).filter(
            model.recipient_id == kwargs['user_id'],
        ).all()

        return items


class Message(Items):
    model = models.Message

    def _get_items(self, session, model, **kwargs):
        message = session.query(model).filter(
            model.id == kwargs['message_id']
        ).all()

        return message
