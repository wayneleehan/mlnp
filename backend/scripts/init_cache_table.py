import sqlite3
import os

# 設定資料庫檔案的路徑 (往上一層回到 backend 根目錄)
# 這樣寫可以確保不管你在哪裡執行這個 script，都能找到 stocks.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'stocks.db')

def init_cache_db():
    print(f"正在連接資料庫: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 建立一個用來存 AI 結果的表
    # stock_id: 股票代碼 (例如 '2330')
    # data: JSON 格式的 AI 分析結果
    # created_at: 建立時間 (用來判斷是否過期)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment_cache (
            stock_id TEXT PRIMARY KEY,
            data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ 快取資料表 (sentiment_cache) 建立完成！")

if __name__ == '__main__':
    init_cache_db()