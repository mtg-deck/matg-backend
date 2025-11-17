from pydantic import BaseModel
from app.schemas.card import Card


class DeckCardBase(BaseModel):
    card_id: str
    quantidade: int
    is_commander: bool

    class Config:
        from_attributes = True


class DeckCardRequest(BaseModel):
    card_name: str
    quantidade: int

    class Config:
        from_attributes = True


class DeckCardQuantity(BaseModel):
    quantidade: int

    class Config:
        from_attributes = True


class DeckCardRead(BaseModel):
    card: Card
    quantidade: int
    is_commander: bool

    class Config:
        from_attributes = True
