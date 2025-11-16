from pydantic import BaseModel
from schemas.deck_card import DeckCardRead


class DeckBase(BaseModel):
    nome: str


class DeckCreate(DeckBase):
    pass


class DeckUpdate(DeckBase):
    pass


class DeckRead(DeckBase):
    id: int
    last_update: str

    class Config:
        from_attributes = True


class DeckWithCards(DeckRead):
    cards: list[DeckCardRead]
