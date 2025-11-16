from pydantic import BaseModel


class Card(BaseModel):
    name: str
    colors: str
    color_identity: str
    cmc: int
    mana_cost: str
    image: str
    art: str
    legal_commanders: bool
    is_commander: bool

    class Config:
        from_attributes = True


class CardRead(Card):
    id: int


class CardList(BaseModel):
    cards: list[Card]
