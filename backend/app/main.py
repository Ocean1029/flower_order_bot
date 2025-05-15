from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.health import router as health_router
from app.routes.orders import api_router as orders_router
from app.routes.statistics import api_router as stats_router
from app.routes.messages import api_router as messages_router
from app.routes.linebot import api_router as linebot_router
from app.routes.export_docx import api_router

app = FastAPI(
    title="花店自動化系統 API",
    description="Backend for LINE Bot & Dashboard",
    version="1.0.0",
    docs_url="/",  # Swagger UI 路徑
    redoc_url="/redoc",  # ReDoc 路徑
    openapi_url="/openapi.json"  # OpenAPI schema 路徑
)

# CORS（可依實際域名收斂設定）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 將 APIRouter 掛進來 =================================================
app.include_router(health_router, tags=["Health"])
app.include_router(orders_router, tags=["Orders"])
app.include_router(messages_router, tags=["Chat"])
app.include_router(stats_router,   tags=["Statistics"])
app.include_router(linebot_router, tags=["LINE Bot Reply Messages"])
app.include_router(api_router)

# === 本地啟動指令 =======================================================
# uvicorn app.main:app --reload --port 8000
# Render 部署：確保 start 命令改成 uvicorn ↑↑
