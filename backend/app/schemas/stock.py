from pydantic import BaseModel

# 股票代碼
class StockResponse(BaseModel):
    code: str
    name: str

    class Config:
        from_attributes = True
        
# 新聞搜尋結果
class NewsResponse(BaseModel):
    title: str          # 標題
    link: str           # 新聞連結
    date: str           # 發布時間
    source: str         # 媒體來源 
    snippet: str        # 摘要 
    
    
# 你的模型輸出結果 你可以自己改這沒差
class AIAnalysisResponse(BaseModel):
    verdict: str   # 結論: "Buy", "Sell", "Hold"
    score: float   # 分數: 0.0 ~ 1.0 或 0 ~ 100
    reason: str    # 理由: "因為..."
    risk: str = "" # 風險 (Optional)