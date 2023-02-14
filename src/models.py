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

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    char_list = relationship(
        'Character',
        secondary=games_and_chars_table,
        back_populates='games'
    )
    state_list = relationship(
        'State',
        secondary=games_and_states_table,
        back_populates='games'
    )
    about = Column(String, nullable=False)


class State(Base):
    __tablename__ = 'states'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    towns_list = relationship('towns', backref='state', lazy=False)
    game_list = relationship(
        'Game',
        secondary=games_and_states_table,
        back_populates='states'
    )


class Town(Base):
    __tablename__ = 'towns'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    borned_list = relationship('characters', backref='Town', lazy=False)


class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dead = Column(Boolean(), nullable=True, default=None)
    bio = Column(String, nullable=False)
    game_list = relationship(
        'Game',
        secondary=games_and_chars_table,
        back_populates='chars'
    )
