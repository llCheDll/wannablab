import hashlib
import jinja2
import os


def row2dict(row):
    return dict([(col.name, str(getattr(row, col.name))) for col in row.__table__.columns])


def load_template(name):
    path = os.path.join('templates', name)
    with open(os.path.abspath(path), 'r') as fp:
        return jinja2.Template(fp.read())


def encrypt(user_credentials, salt):
    return hashlib.pbkdf2_hmac('sha256', user_credentials.encode(), salt.encode(), 100000).hex()


def parse_data(request):
    json_data = []
    data = request.bounded_stream.read().decode('utf-8')
    data = data.replace('=', ':').split('&')

    for item in data:
        json_data.append(item.split(':'))

    json_data = dict(json_data)

    json_data['psw'] = encrypt(json_data['psw'], 'ololo')

    return json_data
