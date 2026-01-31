import { useState, useEffect } from 'react';
import './SearchBar.css';

function SearchBar({ onSearch }) {
  const [inputValue, setInputValue] = useState('');     // 使用者輸入的字
  const [suggestions, setSuggestions] = useState([]);   // 後端回傳的建議名單
  const [showSuggestions, setShowSuggestions] = useState(false); // 是否顯示選單
  const [isLoading, setIsLoading] = useState(false);    // 載入狀態

  // 使用 useEffect 實作 "防抖 (Debounce)"
  // 當 inputValue 改變時，不會馬上發送，而是設定一個 300ms 的計時器
  useEffect(() => {
    // 1. 如果輸入是空的，清空建議並結束
    if (!inputValue.trim()) {
      setSuggestions([]);
      return;
    }

    // 2. 設定計時器
    const timerId = setTimeout(async () => {
      setIsLoading(true); // 開始載入
      try {
        // 注意：這裡是連線到 FastAPI 的 Port 8000
        const response = await fetch(`http://localhost:8000/api/stocks/search?query=${inputValue}`);
        
        if (response.ok) {
          const data = await response.json();
          setSuggestions(data);
          setShowSuggestions(true);
        } else {
            console.error("後端回應錯誤:", response.status);
        }
      } catch (error) {
        console.error("無法連線到後端:", error);
      } finally {
        setIsLoading(false); // 無論成功失敗，都要結束載入狀態
      }
    }, 300); // 延遲 300 毫秒

    // 3. 清除函式 (Cleanup Function)
    // 如果使用者在 300ms 內又打字了，React 會執行這行，把上一次的計時器取消
    // 這就是防抖的核心！
    return () => clearTimeout(timerId);

  }, [inputValue]); // 監聽 inputValue 的變化

  // 處理點擊建議選項
  const handleSelectSuggestion = (stock) => {
    const value = `${stock.code} ${stock.name}`;
    setInputValue(value);
    onSearch(stock.code); // 傳遞代碼給父層
    setShowSuggestions(false);
  };

  return (
    <div className="search-container">
      <div className="input-wrapper">
        <input 
          type="text" 
          className="search-input"
          placeholder="輸入股票代碼 (例: 2330)" 
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onFocus={() => { if(suggestions.length > 0) setShowSuggestions(true); }}
          // 失去焦點時延遲關閉，讓使用者有時間點擊選項
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
        />
        
        {/* 顯示載入中的小圈圈 (UX 優化) */}
        {isLoading && <div className="loading-indicator">搜尋中...</div>}

        {/* 建議選單 */}
        {showSuggestions && suggestions.length > 0 && (
          <ul className="suggestions-list">
            {suggestions.map((stock) => (
              <li 
                key={stock.code} 
                onClick={() => handleSelectSuggestion(stock)}
                className="suggestion-item"
              >
                <span className="stock-code">{stock.code}</span>
                <span className="stock-name">{stock.name}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <button className="search-button" onClick={() => onSearch(inputValue)}>
        分析
      </button>
    </div>
  );
}

export default SearchBar;