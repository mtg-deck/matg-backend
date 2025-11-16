from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base


class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    last_update = Column(DateTime, nullable=False)

    cards = relationship(
        "DeckCard", back_populates="deck", cascade="all, delete-orphan"
    )
