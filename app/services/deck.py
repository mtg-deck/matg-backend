from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.orm import joinedload, selectinload
from datetime import datetime
from fastapi import HTTPException
from io import StringIO
import csv

from app.models.deck import Deck
from app.models.deck_card import DeckCard
from app.models.card import Card
from app.schemas.deck import DeckCreate, DeckUpdate, DeckRead
from app.schemas.deck_card import DeckCardRead


# ===========================================
# BASIC DECK FETCHING
# ===========================================


async def list_decks(db: AsyncSession):
    result = await db.execute(select(Deck))
    return result.scalars().all()


async def get_deck_by_name(name: str, db: AsyncSession):
    result = await db.execute(select(Deck).where(Deck.nome == name))
    return result.scalar_one_or_none()


async def get_deck_by_id(id: int, db: AsyncSession):
    result = await db.execute(select(Deck).where(Deck.id == id))
    return result.scalar_one_or_none()


async def get_deck_with_cards(id: int, db: AsyncSession):
    result = await db.execute(
        select(Deck)
        .options(selectinload(Deck.cards).selectinload(DeckCard.card))
        .where(Deck.id == id)
    )

    return result.scalar_one_or_none()


async def get_deck_with_cards_by_name(name: str, db: AsyncSession):
    result = await db.execute(
        select(Deck)
        .options(joinedload(Deck.cards).joinedload(DeckCard.card))
        .where(Deck.nome == name)
    )
    result = result.unique()
    return result.scalar_one_or_none()


async def get_deck_read(id: int, db: AsyncSession):
    deck = await get_deck_with_cards(id, db)
    return deck


# ===========================================
# CREATE / UPDATE / DELETE
# ===========================================


async def create_deck(data: DeckCreate, db: AsyncSession):
    deck = Deck(nome=data.nome, last_update=datetime.now())
    db.add(deck)
    await db.commit()
    await db.refresh(deck)
    return deck


async def update_deck(deck_id: int, data: DeckUpdate, db: AsyncSession):
    deck = await get_deck_by_id(deck_id, db)
    if not deck:
        return None

    deck.nome = data.nome
    deck.last_update = datetime.now()

    await db.commit()
    await db.refresh(deck)
    return deck


async def delete_deck(deck_id: int, db: AsyncSession):
    deck = await get_deck_by_id(deck_id, db)
    if not deck:
        return False

    await db.delete(deck)
    await db.commit()
    return True


# ===========================================
# DECK CARD OPERATIONS
# ===========================================


async def add_card(
    deck_id: int, card_id: str, quantidade: int, is_commander: bool, db: AsyncSession
):
    result = await db.execute(
        select(DeckCard).where(DeckCard.deck_id == deck_id, DeckCard.card_id == card_id)
    )

    existing = result.scalar_one_or_none()

    if existing:
        existing.quantidade += quantidade
        await db.commit()
        await db.refresh(existing)
        result = await db.execute(
            select(DeckCard)
            .options(selectinload(DeckCard.card))
            .where(DeckCard.deck_id == deck_id, DeckCard.card_id == card_id)
        )
        return result.scalar_one()

    dc = DeckCard(
        deck_id=deck_id,
        card_id=card_id,
        quantidade=quantidade,
        is_commander=is_commander,
    )
    db.add(dc)
    await db.commit()
    await db.refresh(dc)

    result = await db.execute(
        select(DeckCard)
        .options(selectinload(DeckCard.card))
        .where(DeckCard.deck_id == deck_id, DeckCard.card_id == card_id)
    )
    return result.scalar_one()


async def update_card_quantity(
    deck_id: int, card_id: str, quantidade: int, db: AsyncSession
):
    result = await db.execute(
        select(DeckCard).where(DeckCard.deck_id == deck_id, DeckCard.card_id == card_id)
    )
    dc = result.scalar_one_or_none()
    if not dc:
        return None

    if dc.is_commander:
        raise HTTPException(400, "Only commander card allowed")

    dc.quantidade = quantidade
    await db.commit()
    await db.refresh(dc)
    return dc


async def remove_card(deck_id: int, card_id: str, db: AsyncSession):
    result = await db.execute(
        select(DeckCard).where(DeckCard.deck_id == deck_id, DeckCard.card_id == card_id)
    )
    dc = result.scalar_one_or_none()
    if not dc:
        return False

    await db.delete(dc)
    await db.commit()
    return True


# ===========================================
# TODO — STATS, EXPORT, IMPORT
# ===========================================


async def get_deck_stats(deck_id: int, db: AsyncSession):
    deck = await get_deck_with_cards(deck_id, db)
    if not deck:
        raise HTTPException(404, "Deck not found")

    stats = {
        "total_cards": sum(c.quantidade for c in deck.cards),
        "cmc_curve": {},
        "colors": {},
        "types": {},
    }

    for dc in deck.cards:
        card = dc.card

        # cmc curve
        stats["cmc_curve"].setdefault(card.cmc, 0)
        stats["cmc_curve"][card.cmc] += dc.quantidade

        # colors
        stats["colors"].setdefault(card.color_identity, 0)
        stats["colors"][card.color_identity] += dc.quantidade

        # types — if you store them
        # stats["types"][...] += ...

    return stats


async def export_txt(deck_id: int, db: AsyncSession):
    deck = await get_deck_with_cards(deck_id, db)
    if not deck:
        raise HTTPException(404, "Deck not found")

    output = StringIO()
    for c in deck.cards:
        output.write(f"{c.quantidade} {c.card.name}\n")

    return output.getvalue()


async def export_csv(deck_id: int, db: AsyncSession):
    deck = await get_deck_with_cards(deck_id, db)
    if not deck:
        raise HTTPException(404, "Deck not found")

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["quantidade", "nome"])
    for c in deck.cards:
        writer.writerow([c.quantidade, c.card.name])

    return output.getvalue()


async def import_txt(file, db: AsyncSession):
    text = (await file.read()).decode("utf-8")

    deck_name = file.filename.replace(".txt", "")
    deck = await create_deck(DeckCreate(nome=deck_name, commander=""), db=db)

    for line in text.splitlines():
        if not line.strip():
            continue

        qnt, name = line.split(" ", 1)
        qnt = int(qnt)

        card = await get_card_by_name_service(name, db)
        if not card:
            continue

        await add_card(deck.id, card.id, qnt, False, db)

    return {"status": "ok", "deck_id": deck.id}


async def import_csv(file, db: AsyncSession):
    text = (await file.read()).decode("utf-8")
    reader = csv.reader(StringIO(text))

    header = next(reader)
    deck_name = file.filename.replace(".csv", "")
    deck = await create_deck(DeckCreate(nome=deck_name, commander=""), db=db)

    for row in reader:
        qnt = int(row[0])
        name = row[1]

        card = await get_card_by_name_service(name, db)
        if not card:
            continue

        await add_card(deck.id, card.id, qnt, False, db)

    return {"status": "ok", "deck_id": deck.id}
