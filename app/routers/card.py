from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.external.api import get_many_cards_from_api
from app.external.edhec import get_edhec_cardlists
from app.database import get_db
from app.schemas.card import Card as CardSchema, CardList, CommanderList
from app.services.card import (
    get_card_by_name_service,
    autocomplete_service,
    get_top_commanders_service,
)
import asyncio

router = APIRouter(prefix="/api/card", tags=["card"])


@router.get("/name/{name}", response_model=CardSchema)
async def get_card_by_name(name: str, db: AsyncSession = Depends(get_db)):
    return await get_card_by_name_service(name, db)


@router.get("/autocomplete/{partial}", response_model=CardList)
async def autocomplete_cards(partial: str, db: AsyncSession = Depends(get_db)):
    return await autocomplete_service(partial, db)


@router.get("/commander", response_model=CardList)
async def get_commanders(db: AsyncSession = Depends(get_db)):
    cards = await get_top_commanders_service(db)
    return cards


@router.get("/commander/{name}/meta", response_model=dict)
async def get_commander_meta(name: str):
    card_list = get_edhec_cardlists(name)

    keys = list(card_list.keys())
    tasks = [get_many_cards_from_api(card_list[key]) for key in keys]

    results = await asyncio.gather(*tasks)

    for key, data in zip(keys, results):
        card_list[key] = data

    return card_list


@router.post("/batch", response_model=CommanderList)
async def get_many_cards(card_list: list[str]):
    if not card_list:
        return []
    cards = await get_many_cards(card_list)
    return cards
