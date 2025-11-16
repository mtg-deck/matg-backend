from sqlalchemy import Boolean, Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from app.database import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    colors = Column(String, nullable=False)
    color_identity = Column(String, nullable=False)
    cmc = Column(Integer, nullable=False)
    mana_cost = Column(String, nullable=False)
    image = Column(String, nullable=False)
    art = Column(String, nullable=False)
    legal_commanders = Column(Boolean, nullable=False)
    is_commander = Column(Boolean, nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)

    decks = relationship("DeckCard", back_populates="card")
