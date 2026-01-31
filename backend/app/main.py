# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# 1. 引入我們寫好的 router
from app.routers import stock 

app = FastAPI()

# --- CORS 設定 (保持原本的) ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 關鍵步驟：把 Router 掛載上去！
# 這樣 /api/stocks/search 才會生效
app.include_router(stock.router)

@app.get("/")
def read_root():
    return {"message": "StockMind AI Backend is running!"}