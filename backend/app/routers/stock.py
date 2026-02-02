from fastapi import APIRouter, Query, HTTPException
from typing import List
# 引入新的 Schema
from app.schemas.stock import StockResponse, NewsResponse, StockAnalysisResult
# 引入 Service
from app.services import stock_service, news_service, ai_service

router = APIRouter(
    prefix="/api/stocks",
    tags=["stocks"]
)

@router.get("/search", response_model=List[StockResponse])
def search_stocks(query: str = Query(..., min_length=1)):
    return stock_service.search_stocks_by_keyword(query)

# [修改] 回傳型別改為 StockAnalysisResult
@router.get("/analyze", response_model=StockAnalysisResult)
def analyze_stock(code: str = Query(..., min_length=2)):
    # 1. 確認股票存在
    stocks = stock_service.search_stocks_by_keyword(code)
    if not stocks:
        raise HTTPException(status_code=404, detail="找不到該股票代碼")
    
    target_stock = stocks[0] # 抓第一筆最符合的
    
    # 2. 搜新聞
    print(f"準備分析: {target_stock.name}")
    news = news_service.search_news_by_keyword(target_stock.name)
    
    # 3. 呼叫 AI 分析 (如果有新聞的話)
    ai_result = None
    if news:
        ai_result = ai_service.analyze_sentiment(target_stock.name, news)

    # 4. 回傳完整結構
    return {
        "stock_info": target_stock,
        "news": news,
        "ai_analysis": ai_result
    }