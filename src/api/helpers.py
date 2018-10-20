import falcon
import jinja2
import os

from datetime import datetime
from urllib.parse import parse_qs
from werkzeug.security import generate_password_hash


def row2dict(row):
    return dict([(col.name, str(getattr(row, col.name))) for col in row.__table__.columns])


def load_template(name):
    path = os.path.join('templates', name)
    with open(os.path.abspath(path), 'r') as fp:
        return jinja2.Template(fp.read())


def logout(request, response, *args, **kwargs):
    if 'COOKIE' in request.headers:
        response.set_cookie(
            'token', '', path='/', secure=False
        )
        response.unset_cookie('token')
        raise falcon.HTTPSeeOther('/api/v1/auth/')


def parse_data(request):
    body = request.stream.read()

    if isinstance(body, bytes):
        body = body.decode()

    body = parse_qs(body)

    return body


def parse_register(request):
    body = request.stream.read()

    if isinstance(body, bytes):
        body = body.decode()

    body = parse_qs(body)

    body['birthday'][0] = datetime.strptime(body['birthday'][0], '%Y-%M-%d').date()
    body['password'][0] = generate_password_hash(body['password'][0])

    return body
