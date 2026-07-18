import sqlite3
import yfinance as yf
from typing import List, Optional
from app.schemas.stock import StockResponse, StockPriceInfo

DB_PATH = 'stocks.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_realtime_price(code: str) -> Optional[StockPriceInfo]:
    """
    使用 yfinance 抓取台股即時股價 (穩定版)
    """
    try:
        # 台股代碼在 Yahoo Finance 需要加上 .TW (上市) 或 .TWO (上櫃)
        # 優先嘗試上市 (.TW)
        target = f"{code}.TW"
        stock = yf.Ticker(target)
        data = stock.history(period="1d")
        
        # 如果沒資料，嘗試上櫃 (.TWO)
        if data.empty:
            target = f"{code}.TWO"
            stock = yf.Ticker(target)
            data = stock.history(period="1d")
        
        if data.empty:
            print(f"❌ yfinance 找不到股價: {code}")
            return None

        # 取得最新一筆資料
        latest = data.iloc[-1]
        
        # 取得前一日收盤價 (計算漲跌用)
        # 嘗試從 info 拿，拿不到就用當日開盤價當作參考
        prev_close = stock.info.get('previousClose')
        if prev_close is None:
            prev_close = latest['Open']

        current_price = latest['Close']
        change = current_price - prev_close
        change_percent = (change / prev_close) * 100 if prev_close != 0 else 0

        return StockPriceInfo(
            price=f"{current_price:.2f}",
            change=f"{change:.2f}",
            change_percent=f"{change_percent:.2f}%",
            open=f"{latest['Open']:.2f}",
            high=f"{latest['High']:.2f}",
            low=f"{latest['Low']:.2f}",
            volume=f"{int(latest['Volume'])}"
        )

    except Exception as e:
        print(f"⚠️ 抓取股價發生錯誤 ({code}): {e}")
        return None

def search_stocks_by_keyword(keyword: str) -> List[StockResponse]:
    """
    從本地資料庫搜尋股票 (僅限台股)
    """
    if not keyword:
        return []

    conn = get_db_connection()
    cursor = conn.cursor()
    # 搜尋代碼或名稱，限制回傳 5 筆
    query = "SELECT code, name FROM stock_list WHERE code LIKE ? OR name LIKE ? LIMIT 5"
    search_pattern = f"%{keyword}%"
    cursor.execute(query, (search_pattern, search_pattern))
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append(StockResponse(code=row['code'], name=row['name'], price_info=None))
    
    return results