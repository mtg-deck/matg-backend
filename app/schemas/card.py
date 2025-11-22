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
    edhec_rank: Optional[str]

    class Config:
        from_attributes = True


class CardList(BaseModel):
    cards: list[Card]
