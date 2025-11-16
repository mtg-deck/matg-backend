from pydantic import BaseModel
from schemas.deck_card import DeckCardRead


class DeckBase(BaseModel):
    nome: str

    class Config:
        orm_mode = True


class DeckCreate(DeckBase):
    pass


class DeckUpdate(DeckBase):
    pass


class DeckRead(DeckBase):
    id: int
    last_update: str


class DeckWithCards(DeckRead):
    cards: list[DeckCardRead]
