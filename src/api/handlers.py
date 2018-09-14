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

    def on_get(self, request, response, **kwargs):
        session = request.context['session']
        items = session.query(self.model).all()

        self.response_to_json(response, items)

    def response_to_json(self, response, items):
        response.set_header('Content-Type', 'application/json')
        response.status = falcon.HTTP_200
        result = [row2dict(item) for item in items]
        if len(result) != 0:
            response.body = ujson.dumps(
                {
                    'status': Status.OK,
                    'data': result
                }
            )
        else:
            response.status = falcon.HTTP_404
            response.body = ujson.dumps(
                {
                    'status': Status.NotFound,
                }
            )


class Category(Items):
    model = models.Category


class Language(Items):
    model = models.Language


class Country(Items):
    model = models.Country


class Region(Items):
    def on_get(self, request, response, **kwargs):
        country_id = kwargs.get('country_id')

        session = request.context['session']
        regions = session.query(models.Region).filter(models.Region.country_id == country_id).all()

        self.response_to_json(response, regions)


class City(Items):
    def on_get(self, request, response, **kwargs):
        country_id = kwargs.get('country_id')
        region_id = kwargs.get('region_id')

        session = request.context['session']
        cities = session.query(models.City).filter(
            models.City.country_id == country_id).filter(models.City.region_id == region_id)

        self.response_to_json(response, cities)


class District(Items):
    def on_get(self, request, response, **kwargs):
        city_id = kwargs.get('city_id')

        session = request.context['session']
        districts = session.query(models.District).filter(models.District.city_id == city_id).all()

        self.response_to_json(response, districts)
