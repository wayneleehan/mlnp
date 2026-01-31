from GoogleNews import GoogleNews

def search_news_by_keyword(keyword: str):
    
    print(f"正在搜尋新聞: {keyword}")
    # 初始化 GoogleNews
    # lang='zh-TW', region='TW' 確保抓到的是台灣繁體中文新聞
    googlenews = GoogleNews(lang='zh-TW', region='TW')
    
    # 搜尋期間設定為過去一週
    googlenews.set_period('7d') 
    googlenews.search(keyword)
    
    # 取得結果前五筆
    results = googlenews.result()[:10]
    
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
            "source": item.get('media', 'Unknown'), # 媒體名稱
            "snippet": item.get('desc', '')         # 摘要
        })
    
    return news_data