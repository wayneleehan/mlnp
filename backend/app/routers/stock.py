from fastapi import APIRouter, Query, HTTPException
from typing import List
from app.schemas.stock import StockResponse, NewsResponse
from app.services import stock_service, news_service 

router = APIRouter(
    prefix="/api/stocks", # 這裡設定前綴，以後這檔案裡的路徑都不用寫 /api/stocks
    tags=["stocks"]       # 在 Swagger UI 上的分類標籤
)

# 搜尋股票的 Endpoint
@router.get("/search", response_model=List[StockResponse])
def search_stocks(query: str = Query(..., min_length=1)):
    # 轉發
    return stock_service.search_stocks_by_keyword(query)

# 分析股票新聞的 Endpoint
@router.get("/analyze", response_model=List[NewsResponse])
def analyze_stock(code: str = Query(..., min_length=2)):
    """
    分析 API：
    1. 用代碼查股票名稱 (2330 -> 台積電)
    2. 搜尋該股票的新聞
    """
    #上面這個也是註解的一種，fastapi 可以開啟一個東西叫 swagger ui，可以查看每一個 api的簡介，這也會顯示在上面，後端啟動後可以用這網址看看，http://127.0.0.1:8000/docs

    # 確認股票存在
    stocks = stock_service.search_stocks_by_keyword(code)
    
    if not stocks:
        # 如果找不到這檔股票，回傳 404
        raise HTTPException(status_code=404, detail="找不到該股票代碼")
    
    # 抓第一筆最符合的名稱
    stock_name = stocks[0].name
    
    # 用「股票名稱」去搜新聞
    # 目前先只搜名稱
    print(f"準備分析: {stock_name}")
    news = news_service.search_news_by_keyword(stock_name)
    
    return news

@router.get("/analyze") # response_model 之後要改成包含 AI 結果的格式
def analyze_stock(code: str):
    # 1. 找股票
    # 2. 找新聞 (news = news_service...)
    # 3. 呼叫 AI 
    # ai_result = ai_service.analyze_sentiment(news)
    # 4. 回傳
    return {
        "news": news,
        "ai_analysis": ai_result
    }