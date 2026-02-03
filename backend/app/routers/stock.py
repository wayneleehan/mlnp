from fastapi import APIRouter, Query, HTTPException
from typing import List
from app.schemas.stock import StockResponse, NewsResponse, StockAnalysisResult
# 引入所有需要的服務
from app.services import stock_service, news_service, ai_service, cache_service

# [關鍵修正] 這一行就是定義 router 的地方，絕對不能少！
router = APIRouter(
    prefix="/api/stocks",
    tags=["stocks"]
)

@router.get("/search", response_model=List[StockResponse])
def search_stocks(query: str = Query(..., min_length=1)):
    return stock_service.search_stocks_by_keyword(query)

@router.get("/analyze", response_model=StockAnalysisResult)
def analyze_stock(code: str = Query(..., min_length=2)):
    # 1. 找基本資料
    stocks = stock_service.search_stocks_by_keyword(code)
    if not stocks:
        raise HTTPException(status_code=404, detail="找不到該股票代碼")
    
    target_stock = stocks[0]
    stock_id = target_stock.code

    # 2. 抓取即時股價，並更新到 target_stock 物件中
    realtime_data = stock_service.get_realtime_price(stock_id)
    target_stock.price_info = realtime_data
    
    # 3. 處理快取與 AI
    cached_result = cache_service.get_cached_sentiment(stock_id)
    
    print(f"準備分析: {target_stock.name}")
    news = news_service.search_news_by_keyword(target_stock.name)
    
    if cached_result:
        return {
            "stock_info": target_stock,
            "news": news,
            "ai_analysis": cached_result
        }

    ai_result = None
    if news:
        ai_result = ai_service.analyze_sentiment(target_stock.name, news)
        if ai_result.verdict != "Error":
            cache_service.save_sentiment(stock_id, ai_result)

    return {
        "stock_info": target_stock,
        "news": news,
        "ai_analysis": ai_result
    }