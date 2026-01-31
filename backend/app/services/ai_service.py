from typing import List
# 這是我定義好的資料格式，你可以去schemas/stock.py 裡面改
from app.schemas.stock import NewsResponse, AIAnalysisResponse 

# 這是你要實作的 function
def analyze_sentiment(news_list: List[NewsResponse]) -> AIAnalysisResponse:
    """
    TODO:在這裡實作模型
    1. news_list 裡面有 5-10 篇新聞，每篇都有 .snippet (摘要) 和 .title (標題)
    2. 把這些文字丟進你的模型
    3. 回傳一個 AIAnalysisResponse 物件
    """
    
    #  看你想要輸出什麼結果出來
    return AIAnalysisResponse(
        verdict="Strong Buy",       # 買入/賣出/持有
        score=score,                # 信心分數 0-100
        reason="近期營收創新高，且外資法人連續買超，顯示市場信心強勁。", # AI 生成的理由
        risk="需注意地緣政治風險對供應鏈的影響。" # 風險提示
    )