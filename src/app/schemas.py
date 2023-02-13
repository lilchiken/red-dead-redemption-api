from typing import List

from pydantic import BaseModel


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


class StateBase(TunedModel):
    state_id: int
    name: str


class GameBase(TunedModel):
    game_id: int
    title: str
    about: str


class GameSchema(GameBase):
    char_list: List[CharBase]
    state_list: List[StateBase]


class StateSchema(StateBase):
    towns_list: List[TownBase]
    game_list: List[GameBase]


class TownSchema(TownBase):
    borned_list: List[CharBase]


class CharSchema(CharBase):
    game_list: List[GameBase]
