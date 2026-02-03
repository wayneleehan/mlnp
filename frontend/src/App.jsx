import { useState } from 'react';
import SearchBar from './components/SearchBar';
import GaugeChart from 'react-gauge-chart';
import './App.css';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  // [新增] 用來強制重置 SearchBar 的 key
  const [resetKey, setResetKey] = useState(0); 

  const handleSearch = async (searchTicker) => {
    // ... (這部分不用動，維持原樣) ...
    setLoading(true);
    setData(null);
    setError(null);
    
    try {
      const response = await fetch(`http://localhost:8000/api/stocks/analyze?code=${searchTicker}`);
      if (!response.ok) throw new Error(`後端回應錯誤: ${response.status}`);
      const result = await response.json();
      setData(result);
    } catch (err) {
      console.error("前端發生錯誤:", err);
      setError(err.message || "發生未知錯誤");
    } finally {
      setLoading(false);
    }
  };

  // [新增] 回到首頁的函式
  const handleReset = () => {
    setData(null);   // 清空資料
    setError(null);  // 清空錯誤
    setLoading(false);
    setResetKey(prev => prev + 1); // 讓 SearchBar 重新渲染 (清空輸入框文字)
  };

  return (
    <div className="app-container">
      {/* [修改] 加上 onClick 事件和 className */}
      <h1 className="app-title" onClick={handleReset} title="回到首頁">
        📈 StockMind AI
      </h1>
      
      {/* [修改] 加上 key，這樣 resetKey 改變時，搜尋框也會被清空 */}
      <SearchBar key={resetKey} onSearch={handleSearch} />

      {/* ... (以下載入中、錯誤、結果顯示區塊都維持原樣，不用動) ... */}
      {loading && <div className="loading">正在分析新聞數據，請稍候...</div>}
      
      {error && (
        <div style={{color: '#ff6b6b', marginTop: '20px', padding: '15px', border: '1px solid #ff6b6b', borderRadius: '8px', background: '#2a1a1a'}}>
          <h3>⚠️ 發生錯誤</h3>
          <p>{error}</p>
        </div>
      )}

      {data && !error && (
        <div className="result-container">
            {/* ... 這裡原本的程式碼都不用動 ... */}
            
            {/* 1. 股價資訊 Header */}
            <div className="stock-header">
                <div className="stock-title">
                    {data.stock_info.name} <span className="stock-code">({data.stock_info.code})</span>
                </div>
                {data.stock_info.price_info ? (
                    <div className={`stock-price ${parseFloat(data.stock_info.price_info.change) >= 0 ? 'up' : 'down'}`}>
                        <span className="current-price">{data.stock_info.price_info.price}</span>
                        <span className="price-change">
                            {parseFloat(data.stock_info.price_info.change) > 0 ? '▲' : '▼'} 
                            {data.stock_info.price_info.change} ({data.stock_info.price_info.change_percent})
                        </span>
                    </div>
                ) : (
                    <div className="stock-price">股價擷取中...</div>
                )}
            </div>

            {/* 2. AI 分析卡片 */}
            {data.ai_analysis ? (
                <div className="card ai-card">
                  <div className="ai-content-wrapper" style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap'}}>
                    <div className="gauge-section" style={{flex: '1', minWidth: '250px', textAlign: 'center', padding: '10px'}}>
                       <h3 style={{marginBottom: '0'}}>AI 信心指數</h3>
                       <GaugeChart id="gauge-chart1" nrOfLevels={3} colors={["#00e676", "#FFC371", "#ff4d4d"]} arcWidth={0.3} percent={data.ai_analysis.score / 100} textColor="#ffffff" needleColor="#aaaaaa" formatTextValue={value => value + '分'} />
                        <div className={`verdict-badge ${data.ai_analysis.verdict}`}>{data.ai_analysis.verdict}</div>
                    </div>
                    <div className="text-section" style={{flex: '1.5', minWidth: '300px', padding: '10px'}}>
                        <p className="reason"><strong>📊 分析摘要：</strong>{data.ai_analysis.reason}</p>
                        <p className="risk"><strong>⚠️ 風險提示：</strong>{data.ai_analysis.risk}</p>
                        <div className="keywords-box" style={{marginTop: '15px'}}>
                            <div className="tags">
                              {(data.ai_analysis.positive_keywords || []).map((w, i) => <span key={i} className="tag p-tag">🔥 {w}</span>)}
                              {(data.ai_analysis.negative_keywords || []).map((w, i) => <span key={i} className="tag n-tag">❄️ {w}</span>)}
                            </div>
                        </div>
                    </div>
                  </div>
                </div>
            ) : (
                <div className="card" style={{padding: '20px'}}><p>本次查詢未產生 AI 分析結果。</p></div>
            )}

            {/* 3. 新聞列表 */}
            <div className="news-section">
                <h3>📰 相關新聞 ({data.news?.length || 0})</h3>
                <div className="news-list">
                  {data.news?.map((item, index) => (
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