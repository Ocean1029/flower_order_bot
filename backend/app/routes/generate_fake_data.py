from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from app.seeds.seed_all import generate_fake_data

api_router = APIRouter()

@api_router.get("/generate-fake-data")
async def generate_data(
    count: int = 10
):
    await generate_fake_data(count)
    return PlainTextResponse("OK")
