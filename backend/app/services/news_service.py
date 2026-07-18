import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

def search_news_by_keyword(keyword: str, max_results: int = 5):
    """
    使用 Google News RSS 抓取新聞 (回傳字典格式以相容 ai_service)
    """
    if not keyword:
        return []

    print(f"正在透過 RSS 搜尋新聞: {keyword}")
    try:
        # 將關鍵字編碼 (例如: 台積電 -> %E5%8F%B0%E7%A9%8D%E9%9B%BB)
        encoded_keyword = urllib.parse.quote(f"{keyword} when:30d")
        
        # Google News RSS 台灣/繁體中文 專屬網址
        url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
        
        # 加上 User-Agent 偽裝成瀏覽器
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        # 發送請求並讀取 XML 資料
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        
        # 解析 XML
        root = ET.fromstring(xml_data)
        news_list = []
        
        # RSS 的新聞內容放在 <channel> 裡的 <item> 標籤中
        for item in root.findall('./channel/item')[:max_results]:
            title = item.find('title').text if item.find('title') is not None else "無標題"
            link = item.find('link').text if item.find('link') is not None else ""
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            source = item.find('source').text if item.find('source') is not None else "Google News"
            
            # [關鍵修改] 這裡改回傳「字典 (Dict)」，配合 ai_service.py 的 .get() 寫法
            news_list.append({
                "title": title,
                "link": link,
                "source": source,
                "date": pub_date,
                "snippet": title
            })
        
        if not news_list:
             print(f"⚠️ 找不到 {keyword} 的新聞")
        else:
             print(f"✅ 成功抓取 {len(news_list)} 篇 {keyword} 的新聞")
             
        return news_list

    except Exception as e:
        print(f"❌ 抓取新聞發生錯誤 ({keyword}): {e}")
        return []