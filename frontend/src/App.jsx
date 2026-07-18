import { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar';
import GaugeChart from 'react-gauge-chart';
import './App.css';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [resetKey, setResetKey] = useState(0); 

  // [新增] 收藏清單狀態 (初始值從 localStorage 讀取)
  const [watchlist, setWatchlist] = useState(() => {
    const saved = localStorage.getItem('stockWatchlist');
    return saved ? JSON.parse(saved) : [];
  });

  // [新增] 加入或移除收藏
  const toggleWatchlist = (stockCode, stockName) => {
    let newList;
    const exists = watchlist.find(item => item.code === stockCode);

    if (exists) {
      // 如果已存在，就移除
      newList = watchlist.filter(item => item.code !== stockCode);
    } else {
      // 如果不存在，就加入
      newList = [...watchlist, { code: stockCode, name: stockName }];
    }

    setWatchlist(newList);
    localStorage.setItem('stockWatchlist', JSON.stringify(newList));
  };

  // [新增] 檢查目前顯示的股票是否已收藏
  const isWatched = (code) => {
    return watchlist.some(item => item.code === code);
  };

  // [新增] 點擊收藏清單項目時，直接搜尋
  const handleWatchlistClick = (code) => {
    // 把代碼填入搜尋框 (選用，或是直接觸發搜尋)
    handleSearch(code);
  };

  // [新增] 刪除單一收藏 (在清單頁面用)
  const removeWatchlistItem = (e, code) => {
    e.stopPropagation(); // 防止觸發點擊搜尋
    const newList = watchlist.filter(item => item.code !== code);
    setWatchlist(newList);
    localStorage.setItem('stockWatchlist', JSON.stringify(newList));
  };

  const handleSearch = async (searchTicker) => {
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

  const handleReset = () => {
    setData(null);
    setError(null);
    setLoading(false);
    setResetKey(prev => prev + 1);
  };

  return (
    <div className="app-container">
      <h1 className="app-title" onClick={handleReset} title="回到首頁">
        📈 StockMind AI
      </h1>
      
      <SearchBar key={resetKey} onSearch={handleSearch} />

      {loading && <div className="loading">正在分析新聞數據，請稍候...</div>}
      
      {error && (
        <div style={{color: '#ff6b6b', marginTop: '20px', padding: '15px', border: '1px solid #ff6b6b', borderRadius: '8px', background: '#2a1a1a'}}>
          <h3>⚠️ 發生錯誤</h3>
          <p>{error}</p>
        </div>
      )}

      {/* [新增] 首頁收藏清單 (當沒有搜尋結果且沒在載入時顯示) */}
      {!data && !loading && !error && (
        <div className="watchlist-section">
            <h3>❤️ 我的自選股 ({watchlist.length})</h3>
            {watchlist.length === 0 ? (
                <p className="empty-hint">你還沒有收藏任何股票，試著搜尋並點擊愛心按鈕吧！</p>
            ) : (
                <div className="watchlist-grid">
                    {watchlist.map((stock) => (
                        <div key={stock.code} className="watchlist-card" onClick={() => handleWatchlistClick(stock.code)}>
                            <div className="card-info">
                                <span className="card-code">{stock.code}</span>
                                <span className="card-name">{stock.name}</span>
                            </div>
                            <button className="remove-btn" onClick={(e) => removeWatchlistItem(e, stock.code)} title="移除">
                                ✕
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
      )}

      {/* 分析結果頁面 */}
      {data && !error && (
        <div className="result-container">
            
            {/* 1. 股價資訊 Header (加入收藏按鈕) */}
            <div className="stock-header">
                <div className="stock-title-group">
                    <div className="stock-title">
                        {data.stock_info.name} <span className="stock-code">({data.stock_info.code})</span>
                    </div>
                    {/* [新增] 收藏按鈕 */}
                    <button 
                        className={`heart-btn ${isWatched(data.stock_info.code) ? 'active' : ''}`}
                        onClick={() => toggleWatchlist(data.stock_info.code, data.stock_info.name)}
                        title={isWatched(data.stock_info.code) ? "移除收藏" : "加入收藏"}
                    >
                        {isWatched(data.stock_info.code) ? '❤️ 已收藏' : '🤍 加入收藏'}
                    </button>
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