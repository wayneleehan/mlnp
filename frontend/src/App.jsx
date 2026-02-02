import { useState } from 'react';
import SearchBar from './components/SearchBar';
import './App.css';

function App() {
  const [data, setData] = useState(null);       // 存放後端回傳的完整資料
  const [loading, setLoading] = useState(false); // 載入狀態

  const handleSearch = async (searchTicker) => {
    setLoading(true);
    setData(null); // 清空舊資料
    
    try {
      // 呼叫我們剛剛改好的 API
      const response = await fetch(`http://localhost:8000/api/stocks/analyze?code=${searchTicker}`);
      const result = await response.json();
      setData(result); // 存入狀態
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>📈 StockMind AI</h1>
      <SearchBar onSearch={handleSearch} />

      {/* 載入中顯示 */}
      {loading && <div className="loading">正在分析新聞數據，請稍候...</div>}

      {/* 有資料時顯示 */}
      {data && (
        <div className="result-container">
          
          {/* AI 分析區塊 */}
          {data.ai_analysis ? (
            <div className="card ai-card">
              <div className="ai-header">
                <h2>AI 投資建議：<span className={`verdict ${data.ai_analysis.verdict}`}>{data.ai_analysis.verdict}</span></h2>
                <div className="score-badge">信心分數: {data.ai_analysis.score}</div>
              </div>
              
              <p className="reason"><strong>分析摘要：</strong>{data.ai_analysis.reason}</p>
              <p className="risk"><strong>風險提示：</strong>{data.ai_analysis.risk}</p>

              {/* 關鍵詞區塊 */}
              <div className="keywords-box">
                <div className="keywords-group">
                  <h4>🔥 正向關鍵詞</h4>
                  <div className="tags">
                    {data.ai_analysis.positive_keywords.map((w, i) => (
                      <span key={i} className="tag p-tag">{w}</span>
                    ))}
                  </div>
                </div>
                <div className="keywords-group">
                  <h4>⚠️ 負向關鍵詞</h4>
                  <div className="tags">
                    {data.ai_analysis.negative_keywords.map((w, i) => (
                      <span key={i} className="tag n-tag">{w}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <p>暫無 AI 分析結果（可能無當日新聞）</p>
          )}

          {/* 新聞列表區塊 */}
          <div className="news-section">
            <h3>📰 相關新聞 ({data.news.length})</h3>
            <div className="news-list">
              {data.news.map((item, index) => (
                <a key={index} href={item.link} target="_blank" rel="noreferrer" className="news-item">
                  <div className="news-title">{item.title}</div>
                  <div className="news-meta">{item.source} • {item.date}</div>
                </a>
              ))}
            </div>
          </div>

        </div>
      )}
    </div>
  );
}

export default App;