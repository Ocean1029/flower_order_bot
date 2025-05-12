from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/health")
async def health():
    return PlainTextResponse("OK")

