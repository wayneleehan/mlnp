import twstock
import sqlite3
import os

# 設定資料庫檔案的路徑 (放在 backend 根目錄)
DB_PATH = 'stocks.db'

def init_db():
    """建立資料庫表結構"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 建立一個簡單的表，只有 code (代碼) 和 name (名稱)
    # create table if not exists 確保重複執行不會報錯
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_list (
            code TEXT PRIMARY KEY,
            name TEXT
        )
    ''')
    
    conn.commit()
    return conn

def fetch_and_save_stocks(conn):
    """從 twstock 套件取得清單並寫入資料庫"""
    cursor = conn.cursor()
    
    print("正在抓取股票清單...")
    
    # twstock.codes 是一個字典，包含了上市櫃所有股票資訊
    # 格式範例: '2330': Ticker(type='股票', code='2330', name='台積電', ...)
    
    stocks_to_insert = []
    
    for code, info in twstock.codes.items():
        # 我們只過濾出 "股票" 類別 (排除權證、ETF 若你不需要的話可以過濾)
        # 這裡示範只抓 "股票" 和 "ETF"
        if info.type in ['股票', 'ETF']:
            stocks_to_insert.append((info.code, info.name))

    print(f"總共找到 {len(stocks_to_insert)} 檔股票/ETF")

    # 批量寫入 (INSERT OR IGNORE 代表如果代碼已存在就跳過，避免重複錯誤)
    cursor.executemany('INSERT OR IGNORE INTO stock_list (code, name) VALUES (?, ?)', stocks_to_insert)
    
    conn.commit()
    print("資料寫入完成！")

if __name__ == '__main__':
    # 確保資料庫可以被建立
    try:
        conn = init_db()
        fetch_and_save_stocks(conn)
        conn.close()
        print(f"成功建立資料庫: {os.path.abspath(DB_PATH)}")
    except Exception as e:
        print(f"發生錯誤: {e}")