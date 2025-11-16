from pydantic import BaseModel


class Card(BaseModel):
    id: str
    colors: str
    color_identity: str
    cmc: int
    mana_cost: str
    image: str
    art: str
    legal_commanders: bool
    is_commander: bool
