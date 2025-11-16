from fastapi import FastAPI
from app.routers.card import router as card_router

app = FastAPI(
    title="Card API",
    version="1.0.0",
)

app.include_router(card_router)


@app.get("/")
async def root():
    return {"status": "ok"}
