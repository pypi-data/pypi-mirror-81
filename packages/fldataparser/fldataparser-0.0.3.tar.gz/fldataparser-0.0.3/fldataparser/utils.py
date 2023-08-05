from .schemas import Location, User
from .exceptions import DecodeException
from typing import Union
from json import loads, dumps


_DATA_TYPES = {'Location': Location, 'User': User}
_EXTRA_FIELD = '_d_type'


def encode_data(data: Union[Location, User]):
    d = data.dict()
    d[_EXTRA_FIELD] = data.__class__.__name__
    return dumps(d)


def decode_data(data: bytes):
    obj = loads(data)
    d_type = obj[_EXTRA_FIELD]
    del obj[_EXTRA_FIELD]

    if d_type in _DATA_TYPES:
        return (d_type, _DATA_TYPES[d_type](**obj))

    raise DecodeException(f"cant parse type '{d_type}' in '{obj}")
