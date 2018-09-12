import ujson
import falcon

from sqlalchemy.orm.exc import NoResultFound
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


class Country(Items):
    model = models.Country


class Region:
    def on_get(self, request, response, country_id):

        try:
            session = request.context['session']
            regions = session.query(models.Region).filter(
                models.Region.country_id == country_id).all()

            response.set_header('Content-Type', 'application/json')
            response.status = falcon.HTTP_200
            response.body = ujson.dumps(
                {
                    'status': Status.OK,
                    'data': [row2dict(region) for region in regions]
                }
            )
        except NoResultFound:
            response.status = falcon.HTTP_404
            response.body = ujson.dumps(
                {
                    'status': Status.NotFound,
                }
            )


class City:
    def on_get(self, request, response, country_id):

        try:
            session = request.context['session']
            cities = session.query(models.City).join(models.Region).filter(
                models.Region.country_id == country_id)

            response.set_header('Content-Type', 'application/json')
            response.status = falcon.HTTP_200
            response.body = ujson.dumps(
                {
                    'status': Status.OK,
                    'data': [row2dict(city) for city in cities]
                }
            )
        except NoResultFound:
            response.status = falcon.HTTP_404
            response.body = ujson.dumps(
                {
                    'status': Status.NotFound,
                }
            )


class District:
    def on_get(self, request, response, city_id):

        try:
            session = request.context['session']
            districts = session.query(models.District).filter(
                models.District.city_id == city_id).all()

            response.set_header('Content-Type', 'application/json')
            response.status = falcon.HTTP_200
            response.body = ujson.dumps(
                {
                    'status': Status.OK,
                    'data': [row2dict(district) for district in districts]
                }
            )
        except NoResultFound:
            response.status = falcon.HTTP_404
            response.body = ujson.dumps(
                {
                    'status': Status.NotFound,
                }
            )
