from pydantic import BaseModel
from typing import List
from datetime import datetime
from .deck_card import DeckCardRead
from .card import Card


class DeckBase(BaseModel):
    nome: str

    class Config:
        from_attributes = True


class DeckCreate(DeckBase):
    commander: str


class DeckUpdate(DeckBase):
    pass


class DeckRead(DeckBase):
    id: int
    last_update: datetime


class DeckWithCards(DeckRead):
    cards: List[DeckCardRead]


class DeckSummary(BaseModel):
    id: int
    nome: str
    last_update: datetime

    class Config:
        from_attributes = True


class DeckList(BaseModel):
    decks: List[DeckSummary]

    class Config:
        from_attributes = True
