from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

from app.schemas.deck import DeckList, DeckCreate, DeckRead, DeckWithCards, DeckUpdate
from app.schemas.deck_card import DeckCardRequest, DeckCardRead
from app.services.card import get_card_by_name_service
from app.services import deck as service

router = APIRouter(prefix="/api/deck", tags=["deck"])

# ============================================
# TODO Implement:
# POST   /deck                Cria um deck manualmente
# GET    /deck/:id            Obtém um deck pelo ID
# PUT    /deck/:id            Atualiza informações do deck
# DELETE /deck/:id            Exclui o deck
# GET    /deck/inicial        Obtém o deck inicial da aplicação
# GET    /deck/name/:name     Obtém um deck pelo nome
# GET    /deck/meta/          Obtém o meta para o deck
# GET    /deck/:id/stats      Retorna estatísticas do deck
# GET    /deck/:id/txt        Baixa o deck como .txt
# GET    /deck/:id/csv        Baixa o deck como .csv
# POST   /deck/import/txt     Cria deck a partir de arquivo .txt
# POST   /deck/import/csv     Cria deck a partir de arquivo .csv
# POST   /deck/:id/card       Adiciona uma carta ao deck
# PUT    /deck/:id/card/:cid  Atualiza quantidade de carta no deck
# DELETE /deck/:id/card/:cid  Remove carta do deck
# ============================================


# ========== LIST ==========
@router.get("/", response_model=DeckList)
async def list_decks(db: AsyncSession = Depends(get_db)):
    decks = await service.list_decks(db)
    return {"decks": decks}


# ========== GET BY ID ==========
@router.get("/{id}", response_model=DeckWithCards)
async def get_deck(id: int, db: AsyncSession = Depends(get_db)):
    deck = await service.get_deck_with_cards(id, db)
    if not deck:
        raise HTTPException(404, "Deck not found")
    return deck


# ========== GET BY NAME ==========
@router.get("/name/{name}", response_model=DeckWithCards)
async def get_deck_by_name(name: str, db: AsyncSession = Depends(get_db)):
    deck = await service.get_deck_with_cards_by_name(name, db)
    if not deck:
        raise HTTPException(404, "Deck not found")
    return deck


# ========== CREATE ==========
@router.post("/", response_model=DeckRead)
async def create_deck(data: DeckCreate, db: AsyncSession = Depends(get_db)):
    commander_card = await get_card_by_name_service(data.commander, db)
    if not commander_card:
        raise HTTPException(400, "Commander not found")

    deck_exists = await service.get_deck_by_name(data.nome, db)
    if deck_exists:
        raise HTTPException(400, "Deck already exists")

    deck = await service.create_deck(data, db)
    await service.add_card(
        deck.id, commander_card.id, quantidade=1, is_commander=True, db=db
    )

    return await service.get_deck_read(deck.id, db)


# ========== UPDATE ==========
@router.put("/{id}", response_model=DeckRead)
async def update_deck(id: int, data: DeckUpdate, db: AsyncSession = Depends(get_db)):
    updated = await service.update_deck(id, data, db)
    if not updated:
        raise HTTPException(404, "Deck not found")
    return updated


# ========== DELETE ==========
@router.delete("/{id}")
async def delete_deck(id: int, db: AsyncSession = Depends(get_db)):
    ok = await service.delete_deck(id, db)
    if not ok:
        raise HTTPException(404, "Deck not found")
    return {"status": "deleted"}


# ========== ADD CARD ==========
@router.post("/{id}/card", response_model=DeckCardRead)
async def add_card(id: int, req: DeckCardRequest, db: AsyncSession = Depends(get_db)):
    card = await get_card_by_name_service(req.card_name, db)
    if not card:
        raise HTTPException(404, "Card not found")

    dc = await service.add_card(id, card.id, req.quantidade, is_commander=False, db=db)
    return dc


# ========== UPDATE CARD ==========
@router.put("/{id}/card/{card_id}", response_model=DeckCardRead)
async def update_card(
    id: int, card_id: str, req: DeckCardRequest, db: AsyncSession = Depends(get_db)
):
    updated = await service.update_card_quantity(id, card_id, req.quantidade, db)
    if not updated:
        raise HTTPException(404, "Card not in deck")
    return updated


# ========== DELETE CARD ==========
@router.delete("/{id}/card/{card_id}")
async def delete_card(id: int, card_id: str, db: AsyncSession = Depends(get_db)):
    ok = await service.remove_card(id, card_id, db)
    if not ok:
        raise HTTPException(404, "Card not found in deck")
    return {"status": "removed"}


# ===============================================================
# TODO implement the following exports/imports:
# ===============================================================


@router.get("/{id}/stats")
async def get_stats(id: int, db: AsyncSession = Depends(get_db)):
    return await service.get_deck_stats(id, db)


@router.get("/{id}/txt")
async def export_txt(id: int, db: AsyncSession = Depends(get_db)):
    return await service.export_txt(id, db)


@router.get("/{id}/csv")
async def export_csv(id: int, db: AsyncSession = Depends(get_db)):
    return await service.export_csv(id, db)


@router.post("/import/txt")
async def import_txt(file: UploadFile, db: AsyncSession = Depends(get_db)):
    return await service.import_txt(file, db)


@router.post("/import/csv")
async def import_csv(file: UploadFile, db: AsyncSession = Depends(get_db)):
    return await service.import_csv(file, db)
