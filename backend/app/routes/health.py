from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/health")
async def health():
    return PlainTextResponse("OK")

@router.get("/")
async def root():
    return PlainTextResponse("Welcome to the API! Please go to /docs to see API docs.")
