import { useState } from 'react';
import SearchBar from './components/SearchBar'; // 引入我們的積木
import './App.css';

function App() {
  const [ticker, setTicker] = useState('');

  // 這個函式會被傳給 SearchBar 使用
  const handleSearch = (searchTicker) => {
    console.log("從子組件收到:", searchTicker);
    setTicker(searchTicker);
    // 這裡之後會呼叫後端 API
  };

  return (
    <div className="app-container">
      <h1>AI 股票分析</h1>
      
      {/* 使用我們做好的組件，把 handleSearch 傳進去 */}
      <SearchBar onSearch={handleSearch} />

      {/* 這裡之後會放「分析結果」的組件 */}
      {ticker && <p>正在分析目標：{ticker}</p>}
    </div>
  );
}

export default App;