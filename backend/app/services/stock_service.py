import sqlite3
import twstock # [確認] 你的 requirements.txt 裡有這個
from typing import List, Optional
from app.schemas.stock import StockResponse, StockPriceInfo

DB_PATH = 'stocks.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# [新增] 抓取即時股價的函式
def get_realtime_price(code: str) -> Optional[StockPriceInfo]:
    try:
        stock = twstock.realtime.get(code)
        if not stock['success']:
            return None
        
        realtime = stock['realtime']
        info = stock['info']
        
        # 處理如果剛開盤還沒成交價的情況，改用開盤價或昨收
        current_price = realtime.get('latest_trade_price') or realtime.get('best_bid_price') or "0"
        
        # 計算漲跌 (twstock有時候沒直接給漲跌幅，我們自己算比較保險)
        # 注意：這裡回傳的都是字串
        previous_close = float(realtime.get('previous_close', 0))
        current_float = float(current_price)
        change = current_float - previous_close
        change_percent = (change / previous_close) * 100 if previous_close != 0 else 0

        return StockPriceInfo(
            price=f"{current_float:.2f}",
            change=f"{change:.2f}",
            change_percent=f"{change_percent:.2f}%",
            open=realtime.get('open', '-'),
            high=realtime.get('high', '-'),
            low=realtime.get('low', '-'),
            volume=realtime.get('accumulate_trade_volume', '0')
        )
    except Exception as e:
        print(f"抓取股價失敗: {e}")
        return None

def search_stocks_by_keyword(keyword: str) -> List[StockResponse]:
    if not keyword:
        return []

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT code, name FROM stock_list WHERE code LIKE ? OR name LIKE ? LIMIT 5"
    search_pattern = f"%{keyword}%"
    cursor.execute(query, (search_pattern, search_pattern))
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        # 這裡我們只回傳基本資料，不用每次搜尋都抓股價(太慢)
        results.append(StockResponse(code=row['code'], name=row['name'], price_info=None))
    
    return results