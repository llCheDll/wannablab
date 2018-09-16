import ujson
import falcon
from sqlalchemy import or_

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


class Event(Items):
    model = models.Event
