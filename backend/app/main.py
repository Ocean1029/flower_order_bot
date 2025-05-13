
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from app.routes.health import router as health_router
from app.routes.index import router as index_router
from app.routes.api_orders import api_router as orders_router
from app.routes.api_messages import api_router as messages_router
from app.routes.api_stats import api_router as stats_router
from app.routes.linebot import api_router as linebot_router

app = FastAPI(
    title="花店自動化系統 API",
    description="Backend for LINE Bot & Dashboard",
    version="1.0.0",
)

# CORS（可依實際域名收斂設定）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 設定靜態檔案
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# === 將 APIRouter 掛進來 =================================================
app.include_router(health_router, tags=["Health"])
app.include_router(index_router,  tags=["Index"])
app.include_router(orders_router, tags=["Orders"])
app.include_router(messages_router, tags=["Messages"])
app.include_router(stats_router,   tags=["Dashboard"])
app.include_router(linebot_router, tags=["LINE Bot"])

for route in app.routes:
    print(f"name={route.name}, path={route.path}")

# === 本地啟動指令 =======================================================
# uvicorn app.main:app --reload --port 8000
# Render 部署：確保 start 命令改成 uvicorn ↑↑
