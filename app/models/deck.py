from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime
from app.database import Base
from datetime import datetime

from app.models.card import Card


class Deck(Base):
    __tablename__ = "decks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, nullable=False, index=True)
    last_update: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    cards: Mapped[list["DeckCard"]] = relationship(
        back_populates="deck",
        cascade="all, delete-orphan",
    )
