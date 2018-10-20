import jwt
import falcon
from sqlalchemy import or_
import ujson

from .constants import Status, JWT_SECRET, JWT_ALGORITHM
from .helpers import row2dict, load_template, logout, parse_data, parse_register
from db import models
from datetime import datetime, timedelta
from base import Session
from werkzeug.security import generate_password_hash, check_password_hash


class Ping:
    def on_get(self, request, response):
        response.set_header('Content-Type', 'application/json')
        response.status = falcon.HTTP_200
        response.body = ujson.dumps({'status': Status.OK})


class Authorization:
    @falcon.before(logout)
    def on_post(self, request, response):
        body = parse_data(request)

        hash_pass = generate_password_hash(body['password'][0])

        model = models.User
        session = request.context['session']

        user = session.query(model).filter_by(
            email=body['email'][0]
        ).one_or_none()

        if user is None or check_password_hash(hash_pass, user.password):
            response.body = ujson.dumps({"message": "Wrong credentialst"})
            response.status = falcon.HTTP_400
            return response

        payload = {
            'user_id': user.id,
            'exp': datetime.now()+timedelta(days=10)
        }

        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

        response.set_cookie(
            'token', jwt_token.decode('utf-8'), path='/', secure=False
        )
        response.status = falcon.HTTP_301

    def on_get(self, request, response):
        if 'COOKIE' in request.headers:
            template = load_template('logout.html')
        else:
            template = load_template('login.html')

        response.status = falcon.HTTP_200
        response.content_type = 'text/html'
        response.body = template.render(something='testing')


class Register:
    def on_post(self, request, response):
        session = Session()
        body = parse_register(request)

        user = models.User(
            first_name=body['first_name'][0],
            last_name=body['last_name'][0],
            gender=body['gender'][0],
            password=body['password'][0],
            birthday=body['birthday'][0],
            email=body['email'][0],
        )
        session.add(user)

        session.commit()

        raise falcon.HTTPSeeOther('/api/v1/auth/')

    def on_get(self, request, response):
        template = load_template('register.html')

        response.status = falcon.HTTP_200
        response.content_type = 'text/html'
        response.body = template.render(something='testing')


class Items:
    model = None

    def on_get(self, request, response, **kwargs):
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
