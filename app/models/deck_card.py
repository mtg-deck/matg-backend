from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base


class DeckCard(Base):
    __tablename__ = "deck_cards"

    deck_id = Column(Integer, ForeignKey("decks.id"), primary_key=True)
    card_id = Column(String, ForeignKey("cards.id"), primary_key=True)

    quantidade = Column(Integer, nullable=False, default=1)

    deck = relationship("Deck", back_populates="cards")
    card = relationship("Card", back_populates="decks")
