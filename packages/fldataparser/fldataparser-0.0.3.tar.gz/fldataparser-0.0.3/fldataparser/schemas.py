from pydantic import BaseModel, validator
from typing import Optional


def _normalize(val: str) -> str:
    if val is None:
        return None
    return val.lower()


class Location(BaseModel):
    name: str
    parent_name: Optional[str] = None

    _name_val = validator('name', allow_reuse=True)(_normalize)
    _parent_name_validator = validator(
        'parent_name', allow_reuse=True
        )(_normalize)


class User(BaseModel):
    fl_id: int
    name: str
    birth_year: int
    gender: Optional[str] = None
    role: Optional[str] = None
    pics: int
    vids: int
    profile_pic_url: Optional[str] = None
    location: Location

    _gender_val = validator('gender', allow_reuse=True)(_normalize)
    _role_val = validator('role', allow_reuse=True)(_normalize)
