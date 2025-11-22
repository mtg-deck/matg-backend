from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean
from app.database import Base


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    colors: Mapped[str] = mapped_column(String, nullable=False)
    color_identity: Mapped[str] = mapped_column(String, nullable=False)
    cmc: Mapped[int] = mapped_column(Integer, nullable=False)
    mana_cost: Mapped[str] = mapped_column(String, nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=False)
    art: Mapped[str] = mapped_column(String, nullable=False)
    legal_commanders: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_commander: Mapped[bool] = mapped_column(Boolean, nullable=False)
    price: Mapped[str] = mapped_column(String, nullable=False)
    edhec_rank: Mapped[str] = mapped_column(String, nullable=True)

    decks: Mapped[list["DeckCard"]] = relationship(back_populates="card")
