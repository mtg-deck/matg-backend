from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey
from app.database import Base


class DeckCard(Base):
    __tablename__ = "deck_cards"

    deck_id: Mapped[int] = mapped_column(ForeignKey("decks.id"), primary_key=True)
    card_id: Mapped[str] = mapped_column(ForeignKey("cards.id"), primary_key=True)

    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_commander: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    deck: Mapped["Deck"] = relationship(back_populates="cards")
    card: Mapped["Card"] = relationship(back_populates="decks")
