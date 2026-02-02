from pydantic import BaseModel
from typing import List, Optional

# 股票代碼 (維持不變)
class StockResponse(BaseModel):
    code: str
    name: str

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

# [新增] 總回應格式：把股票資訊、新聞、AI分析包在一起
class StockAnalysisResult(BaseModel):
    stock_info: StockResponse
    news: List[NewsResponse]
    ai_analysis: Optional[AIAnalysisResponse] = None