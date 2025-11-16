from pydantic import BaseModel
from schemas.card import Card


class DeckCardBase(BaseModel):
    card_id: int
    quantidade: int

    class Config:
        orm_mode = True


class DeckCardCreate(DeckCardBase):
    pass


class DeckCardRead(BaseModel):
    card: Card
    quantidade: int

    class Config:
        from_attributes = True
