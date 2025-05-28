# Makefile

# 標記這些目標為 phony，不對應到實際檔案
.PHONY: all install migrate run

# 預設目標：依序執行 install → migrate → run
all: install migrate run

# 安裝相依套件
install:
	pip install -r requirements.txt

# 執行 Alembic 資料庫遷移
migrate:
	alembic upgrade head

# 啟動 Uvicorn 開發伺服器
run:
	uvicorn app.main:app --reload
