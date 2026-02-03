from GoogleNews import GoogleNews
from urllib.parse import urljoin

def clean_url(url: str) -> str:
    """
    清除網址中多餘的 Google 追蹤參數，避免造成 404 錯誤
    """
    # 許多錯誤連結都是因為直接黏上了 &ved= 或 &usg=
    if "&ved=" in url:
        url = url.split("&ved=")[0]
    if "&usg=" in url:
        url = url.split("&usg=")[0]
    return url

def search_news_by_keyword(keyword: str):
    print(f"正在搜尋新聞: {keyword}")
    googlenews = GoogleNews(lang='zh-TW', region='TW')
    googlenews.set_period('1d') 
    googlenews.search(keyword)
    
    results = googlenews.result()

    if not results:
        print("當天無新聞，嘗試擴大搜尋範圍至 7 天...")
        googlenews.clear()
        googlenews.set_period('7d')
        googlenews.search(keyword)
        results = googlenews.result()
    
    # 抓 10 篇
    results = results[:10]
    
    news_data = []
    for item in results:
        title = item.get('title', '')
        if not title:
            continue
        
        raw_link = item.get('link', '')
        
        # 1. 先處理相對路徑 (./articles/...)
        full_link = urljoin("https://news.google.com", raw_link)
        
        # 2. [新增] 清理追蹤參數，修復 404 問題
        final_link = clean_url(full_link)

        # 除錯用：印出來看看修正前後的差異
        if raw_link != final_link:
            print(f"修復連結: {raw_link} -> {final_link}")

        news_data.append({
            "title": title,
            "link": final_link, # 使用清理過的連結
            "date": item.get('date', ''),
            "source": item.get('media', 'Unknown'),
            "snippet": item.get('desc', '')
        })
    
    return news_data