from pydantic import BaseModel
from typing import Optional


class Card(BaseModel):
    id: str
    name: str
    colors: str
    color_identity: str
    cmc: int
    mana_cost: str
    image: str
    art: str
    legal_commanders: bool
    is_commander: bool
    price: str
    edhrec_rank: Optional[int]

    class Config:
        from_attributes = True


class CardList(BaseModel):
    cards: list[Card]


class Commander(Card):
    commander_rank: Optional[int] = None


class CommanderList(BaseModel):
    cards: list[Commander]
