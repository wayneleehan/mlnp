from fastapi import APIRouter, Query
from typing import List
from app.schemas.stock import StockResponse
from app.services import stock_service

router = APIRouter(
    prefix="/api/stocks", # 這裡設定前綴，以後這檔案裡的路徑都不用寫 /api/stocks
    tags=["stocks"]       # 在 Swagger UI 上的分類標籤
)

@router.get("/search", response_model=List[StockResponse])
def search_stocks(query: str = Query(..., min_length=1)):
    # Router 只做「轉發」的工作，不做邏輯運算
    return stock_service.search_stocks_by_keyword(query)