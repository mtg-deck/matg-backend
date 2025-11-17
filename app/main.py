from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from app.database import engine, Base
from app.routers.card import router as card_router
from app.routers.deck import router as deck_router

app = FastAPI(
    title="Card API",
    version="1.0.0",
)

app.include_router(card_router)
app.include_router(deck_router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"status": "ok"}
