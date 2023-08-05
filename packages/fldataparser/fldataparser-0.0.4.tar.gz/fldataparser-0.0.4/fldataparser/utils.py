from .schemas import Location, User
from .exceptions import DecodeException
from typing import Union
from json import loads, dumps


DATA_TYPES = {'Location': Location, 'User': User}
EXTRA_FIELD = '_d_type'


def encode_data(data: Union[Location, User]):
    d = data.dict()
    d[EXTRA_FIELD] = data.__class__.__name__
    return dumps(d)


def decode_data(data: bytes):
    obj = loads(data)
    d_type = obj[EXTRA_FIELD]
    del obj[EXTRA_FIELD]

    if d_type in DATA_TYPES:
        return (d_type, DATA_TYPES[d_type](**obj))

    raise DecodeException(f"cant parse type '{d_type}' in '{obj}")
