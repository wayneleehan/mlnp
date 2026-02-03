import sqlite3
import json
import os
from datetime import datetime, timedelta
from app.schemas.stock import AIAnalysisResponse

# 設定資料庫路徑 (往上一層回到 backend 根目錄找到 stocks.db)
# 這裡使用相對路徑技巧，確保不管在哪裡執行都能找到
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'stocks.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_cached_sentiment(stock_id: str):
    """
    嘗試取得有效的快取。
    設定有效期限為 1 小時 (3600秒)。
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 找該股票的快取
        cursor.execute('SELECT data, created_at FROM sentiment_cache WHERE stock_id = ?', (stock_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            # 檢查是否過期 (例如 1 小時前)
            cached_time = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
            if datetime.now() - cached_time < timedelta(hours=1):
                print(f"✅ 發現有效快取 (建立於 {row['created_at']})，跳過 AI 呼叫！")
                # 把存的 JSON 字串轉回 Pydantic 物件
                data_dict = json.loads(row['data'])
                return AIAnalysisResponse(**data_dict)
            else:
                print(f"⚠️ 快取已過期 (建立於 {row['created_at']})，準備重新分析...")
        
        return None
    except Exception as e:
        print(f"讀取快取失敗 (可能是資料表還沒建立): {e}")
        return None

def save_sentiment(stock_id: str, ai_result: AIAnalysisResponse):
    """
    將 AI 結果存入資料庫
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 轉成 JSON 字串
        json_data = json.dumps(ai_result.model_dump(), ensure_ascii=False)
        
        # 使用 REPLACE INTO (如果存在就更新，不存在就插入)
        # 並更新時間為現在
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            REPLACE INTO sentiment_cache (stock_id, data, created_at)
            VALUES (?, ?, ?)
        ''', (stock_id, json_data, now))
        
        conn.commit()
        conn.close()
        print("💾 AI 分析結果已寫入快取資料庫")
    except Exception as e:
        print(f"寫入快取失敗: {e}")