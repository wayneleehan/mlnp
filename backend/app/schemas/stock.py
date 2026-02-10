from pydantic import BaseModel
from typing import List, Optional

# [新增] 股價資訊格式
class StockPriceInfo(BaseModel):
    price: str          # 現價
    change: str         # 漲跌價差
    change_percent: str # 漲跌幅
    open: str           # 開盤
    high: str           # 最高
    low: str            # 最低
    volume: str         # 成交量

# 股票代碼 (維持不變)
class StockResponse(BaseModel):
    code: str
    name: str
    price_info: Optional[StockPriceInfo] = None

    class Config:
        from_attributes = True
        
# 新聞搜尋結果 (維持不變)
class NewsResponse(BaseModel):
    title: str
    link: str
    date: str
    source: str
    snippet: str
    
# [修改] AI 分析結果：加入關鍵詞欄位
class AIAnalysisResponse(BaseModel):
    verdict: str            # 結論: "Buy", "Sell", "Hold"
    score: float            # 分數: 0 ~ 100
    reason: str             # 理由
    risk: str = ""          # 風險
    positive_keywords: List[str] = [] # [新增] 正向關鍵詞
    negative_keywords: List[str] = [] # [新增] 負向關鍵詞

# 總回應格式
class StockAnalysisResult(BaseModel):
    stock_info: StockResponse
    news: List[NewsResponse]
    ai_analysis: Optional[AIAnalysisResponse] = None