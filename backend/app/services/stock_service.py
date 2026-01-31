import sqlite3
from typing import List
from app.schemas.stock import StockResponse

# 設定資料庫路徑 (注意：這裡的路徑要根據你的執行位置微調，建議用絕對路徑或相對路徑)
DB_PATH = 'stocks.db' 

def get_db_connection():
    # check_same_thread=False 是為了讓 FastAPI 多執行緒讀取 SQLite 不會報錯
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row # 讓程式可以用欄位名稱 (row['code']) 來取值
    return conn

def search_stocks_by_keyword(keyword: str) -> List[StockResponse]:
    if not keyword:
        return []

    conn = get_db_connection()
    cursor = conn.cursor()

    # 使用 SQL 的 LIKE 語法進行模糊搜尋
    # % 代表萬用字元
    # 同時搜尋 代碼和名稱
    query = """
        SELECT code, name 
        FROM stock_list 
        WHERE code LIKE ? OR name LIKE ? 
        LIMIT 10
    """
    
    # 模糊搜尋
    search_pattern = f"%{keyword}%" 

    
    cursor.execute(query, (search_pattern, f"%{keyword}%")) # code 用開頭匹配，name 用包含匹配
    rows = cursor.fetchall()
    
    conn.close()

    # 轉換成 Schema 格式回傳
    results = [
        StockResponse(code=row['code'], name=row['name']) 
        for row in rows
    ]
    
    return results