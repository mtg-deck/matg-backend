from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.card import Card
from app.schemas.card import Card, CardList
from app.external.api import get_card_from_api, get_autocomplete_from_api
from app.database import get_db

# TODO: implement
# GET /card/commander       Obtém os 100 commanders melhores ranqueados


router = APIRouter(prefix="/api/card", tags=["card"])


@router.get("/name/{name}", response_model=Card)
async def get_card_by_name(name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Card).where(Card.name == name))
    card = result.scalar_one_or_none()

    if card:
        return card

    api_card = await get_card_from_api(name)
    return api_card


@router.get("/autocomplete/{partial}", response_model=CardList)
async def autocomplete_cards(partial: str):
    return await get_autocomplete_from_api(partial)


@router.get("/commander", response_model=CardList)
async def get_commanders():
    raise HTTPException(501, "Not implemented")
