from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.error_code import ServerError
from datetime import date, datetime


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %M:%H:%S')
        print(type(o))
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder