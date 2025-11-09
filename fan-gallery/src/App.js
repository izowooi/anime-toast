import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Gallery from './pages/Gallery';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Gallery />} />
        <Route path="/character/:id" element={<CharacterDetailPlaceholder />} />
      </Routes>
    </Router>
  );
}

// 상세 페이지 플레이스홀더 (나중에 구현)
function CharacterDetailPlaceholder() {
  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h1>캐릭터 상세 페이지</h1>
      <p>이 페이지는 나중에 구현될 예정입니다.</p>
      <a href="/" style={{ color: '#3b82f6' }}>갤러리로 돌아가기</a>
    </div>
  );
}

export default App;
