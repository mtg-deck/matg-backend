from app.schemas.card import Commander
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql.operators import op
from app.models.card import Card as CardModel
from app.external.api import (
    get_card_from_api,
    get_autocomplete_from_api,
    get_commanders_from_api,
    get_many_cards_from_api,
)


async def get_card_by_name_service(name: str, db: AsyncSession):
    result = await db.execute(select(CardModel).where(CardModel.name == name))
    card = result.scalar_one_or_none()

    if card:
        return card

    api_card = await get_card_from_api(name)
    card = CardModel(**api_card)

    db.add(card)
    await db.commit()
    await db.refresh(card)

    return card


async def autocomplete_service(partial: str, db: AsyncSession):
    cards = await get_autocomplete_from_api(partial)

    for c in cards["cards"]:
        obj = CardModel(**c)
        await db.merge(obj)

    await db.commit()
    return cards


async def get_top_commanders_service(db: AsyncSession):
    cards = await get_commanders_from_api()
    for c in cards["cards"]:
        obj = card_from_commander(Commander(**c))
        await db.merge(obj)
    return cards


def card_from_commander(commander: Commander) -> CardModel:
    return CardModel(
        id=commander.id,
        name=commander.name,
        colors=commander.colors,
        color_identity=commander.color_identity,
        cmc=commander.cmc,
        mana_cost=commander.mana_cost,
        image=commander.image,
        art=commander.art,
        legal_commanders=commander.legal_commanders,
        price=commander.price,
        is_commander=commander.is_commander,
        edhrec_rank=commander.edhrec_rank,
    )


async def get_many_cards_service(card_list, db: AsyncSession):
    cards = await get_many_cards_from_api(card_list)
    for c in cards["cards"]:
        obj = CardModel(**c)
        await db.merge(obj)
    return cards
