import re
from typing import ForwardRef, Union

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import constr
from pydantic import validator


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class CharBase(TunedModel):
    char_id: int
    name: str
    dead: bool
    bio: str


class TownBase(TunedModel):
    town_id: int
    name: str

