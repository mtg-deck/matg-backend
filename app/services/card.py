from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.card import Card as CardModel
from app.schemas.card import Card as CardSchema, CardList
from app.external.api import get_card_from_api, get_autocomplete_from_api


async def get_card_by_name_service(name: str, db: AsyncSession) -> CardSchema:
    result = await db.execute(select(CardModel).where(CardModel.name == name))
    card = result.scalar_one_or_none()

    if card:
        return card

    api_card = await get_card_from_api(name)
    print(api_card)
    card = CardModel(**api_card)

    db.add(card)
    await db.commit()
    await db.refresh(card)

    return card


async def autocomplete_service(partial: str) -> CardList:
    return await get_autocomplete_from_api(partial)


async def get_top_commanders_service():
    raise HTTPException(status_code=501, detail="Not implemented")
