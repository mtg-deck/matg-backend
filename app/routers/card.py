from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.card import Card as CardSchema, CardList
from app.services.card import (
    get_card_by_name_service,
    autocomplete_service,
    get_top_commanders_service,
)

router = APIRouter(prefix="/api/card", tags=["card"])


@router.get("/name/{name}", response_model=CardSchema)
async def get_card_by_name(name: str, db: AsyncSession = Depends(get_db)):
    return await get_card_by_name_service(name, db)


@router.get("/autocomplete/{partial}", response_model=CardList)
async def autocomplete_cards(partial: str):
    return await autocomplete_service(partial)


@router.get("/commander", response_model=CardList)
async def get_commanders():
    return await get_top_commanders_service()
