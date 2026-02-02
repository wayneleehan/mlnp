from google import genai
from google.genai import types # 引入 types 以便設定錯誤處理
import json
import os
import time # [新增] 引入 time 用來休息
from typing import List
from app.schemas.stock import NewsResponse, AIAnalysisResponse

# 你的 API KEY
GENAI_API_KEY = "Upload your own Google API key" 

client = genai.Client(api_key=GENAI_API_KEY)

def analyze_sentiment(stock_name: str, news_list: List[dict]) -> AIAnalysisResponse:
    
    if not news_list:
        return AIAnalysisResponse(
            verdict="Neutral", score=50, reason="無新聞資料可供分析", risk="", positive_keywords=[], negative_keywords=[]
        )

    # 1. 準備新聞內容
    news_text = ""
    for idx, news in enumerate(news_list):
        title = news.get('title', '無標題')
        snippet = news.get('snippet', '無摘要')
        news_text += f"{idx+1}. {title} - {snippet}\n"

    # 2. Prompt
    prompt = f"""
    你是一位專業的股票分析師。請根據以下關於「{stock_name}」的新聞，進行情緒分析。
    
    新聞內容：
    {news_text}

    請嚴格遵守以下 JSON 格式回傳（不要使用 Markdown，只要純 JSON 字串）：
    {{
        "verdict": "Buy" 或 "Sell" 或 "Hold",
        "score": 0到100的整數 (100為極度看好),
        "reason": "一段約50-100字的繁體中文綜合分析",
        "risk": "一段簡短的風險提示",
        "positive_keywords": ["詞彙1", "詞彙2", ...],
        "negative_keywords": ["詞彙1", "詞彙2", ...]
    }}
    """

    # [修改] 加入重試邏輯 (最多試 3 次)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"呼叫 AI 模型中... (第 {attempt + 1} 次嘗試)")
            
            response = client.models.generate_content(
                model='gemini-2.0-flash', 
                contents=prompt
            )
            
            # 成功取得回應，處理資料
            text = response.text.replace("```json", "").replace("```", "").strip()
            result_json = json.loads(text)
            return AIAnalysisResponse(**result_json)

        except Exception as e:
            error_str = str(e)
            # 如果是 429 (Resource Exhausted) 錯誤，就休息後重試
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                print(f"遭遇 429 限流，等待 10 秒後重試...")
                time.sleep(10) # 休息 10 秒
                continue # 進入下一次迴圈重試
            else:
                # 如果是其他錯誤 (如 API Key 錯)，直接放棄
                print(f"AI 分析發生無法挽回的錯誤: {e}")
                break

    # 如果試了 3 次都失敗，回傳錯誤訊息
    return AIAnalysisResponse(
        verdict="Error", 
        score=0, 
        reason="AI 服務忙碌中，請稍後再試 (Rate Limit Exceeded)", 
        risk="請檢查 API Quota 或稍候重試", 
        positive_keywords=[], 
        negative_keywords=[]
    )