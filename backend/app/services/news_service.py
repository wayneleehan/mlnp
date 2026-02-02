from GoogleNews import GoogleNews

def search_news_by_keyword(keyword: str):
    print(f"正在搜尋新聞: {keyword}")
    # lang='zh-TW', region='TW' 確保抓到的是台灣繁體中文新聞
    googlenews = GoogleNews(lang='zh-TW', region='TW')
    
    # [修改] 設定為 '1d' 代表過去 24 小時 (當天)
    googlenews.set_period('1d') 
    googlenews.search(keyword)
    
    results = googlenews.result()

    # [新增] 如果當天沒新聞，為了不讓畫面空白，自動切換成抓 7 天
    if not results:
        print("當天無新聞，嘗試擴大搜尋範圍至 7 天...")
        googlenews.clear()
        googlenews.set_period('7d')
        googlenews.search(keyword)
        results = googlenews.result()
    
    # 限制前 10 筆，避免 AI 讀太久或 token 爆掉
    results = results[:10]
    
    # 資料清洗
    news_data = []
    for item in results:
        # GoogleNews 有時候會回傳空標題，過濾掉
        if not item.get('title'):
            continue
            
        news_data.append({
            "title": item.get('title'),
            "link": item.get('link'),
            "date": item.get('date'),
            "source": item.get('media', 'Unknown'),
            "snippet": item.get('desc', '')
        })
    
    return news_data