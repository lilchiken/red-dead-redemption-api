import uuid

from sqlalchemy import Boolean, Column, String, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

games_and_chars_table = Table(
    'games_and_chars_table',
    Base.metadata,
    Column('game_id', ForeignKey('games.id'), primary_key=True),
    Column('character_id', ForeignKey('characters.id'), primary_key=True),
)

games_and_states_table = Table(
    'games_and_states_table',
    Base.metadata,
    Column('game_id', ForeignKey('games.id'), primary_key=True),
    Column('state_id', ForeignKey('states.id'), primary_key=True),
)


class Game(Base):
    __tablename__ = 'games'

    game_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    char_list = relationship('characters',
                             secondary=games_and_chars_table,
                             backref='Game')

    state_list = relationship('states',
                              secondary=games_and_states_table,
                              backref='Game')

    about = Column(String, nullable=False)


class State(Base):
    __tablename__ = 'states'

    state_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    towns_list = relationship('towns', uselist=True, backref='State')


class Town(Base):
    __tablename__ = 'towns'

    town_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    borned_list = relationship('characters', uselist=True, backref='Town')


class Character(Base):
    __tablename__ = 'characters'

    char_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dead = Column(Boolean(), nullable=False, default=False)
    bio = Column(String, nullable=False)
