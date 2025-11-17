import httpx
from app.config import settings

headers = {
    "x-api-key": settings.API_KEY,
    "x-client-id": settings.CLIENT_ID,
}


async def get_card_from_api(name: str) -> dict:
    url = f"{settings.API_URL}/api/cards/{name}"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP error fetching card: {e.response.status_code}")
        except httpx.RequestError as e:
            raise Exception(f"Error connecting to API: {str(e)}")


async def get_autocomplete_from_api(partial: str) -> dict:
    url = f"{settings.API_URL}/api/cards/autocomplete/{partial}"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"HTTP error fetching autocomplete: {e.response.status_code}"
            )
        except httpx.RequestError as e:
            raise Exception(f"Error connecting to API: {str(e)}")


async def get_many_cards_from_api(cards: list[str]) -> dict:
    url = f"{settings.API_URL}/api/cards/"
    payload = {"cards": cards}

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"HTTP error fetching multiple cards: {e.response.status_code}"
            )
        except httpx.RequestError as e:
            raise Exception(f"Error connecting to API: {str(e)}")


async def get_commanders_from_api() -> dict:
    """Ainda não implementado porque falta endpoint"""
    raise NotImplementedError("Commander endpoint not implemented yet")
