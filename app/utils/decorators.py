import functools

from flask import request
from flask_restplus import reqparse, abort


def parse_request(*args,**kwargs):
    """
    Decorator used to parse request
    :param args: list of Arguments (flask_restful.reqparse.Argument)
    :param kwargs:
    :return:
    """
    parser = reqparse.RequestParser(bundle_errors=True)
    for arg in args:
        parser.add_argument(arg)

    if kwargs.get('allow_ordering', None):
        parser_args = [p.name for p in parser.args]
        default_args = [
            reqparse.Argument("sort_by", type=str, store_missing=False),
            reqparse.Argument("order", type=str, store_missing=False, choices=('asc', 'desc')),
        ]
        for p in default_args:
            if p.name not in parser_args:
                parser.add_argument(p)

    def decorator(f):
        @functools.wraps(f)
        def inner(*fargs, **fkwargs):
            fkwargs.update(parser.parse_args())
            return f(*fargs, **fkwargs)

        return inner

    return decorator


def parse_with(schema, arg_name='entity', **kwargs):
    """Decorator used to parse json input using the specified schema
    :param kwargs will be passed down to the dump method from marshmallow Schema
    :param arg_name will be inserted as a keyword argument containing the
        deserialized data.
    """
    def decorator(f):
        @functools.wraps(f)
        def inner(*fargs, **fkwargs):
            json = request.get_json() or {}
            entity, errors = schema.load(json, **kwargs)
            fkwargs.update({arg_name: entity})
            return f(*fargs, **fkwargs)
        return inner
    return decorator

def HasApiKey(parser):
    def decorator(f):
        @functools.wraps(f)
        def inner(*fargs, **fkwargs):

            args = parser.parse_args()
            if args["API_KEY"]:
                return f(*fargs, **fkwargs)
            abort(401,message="Unauthorized access")
        return inner

    return decorator
