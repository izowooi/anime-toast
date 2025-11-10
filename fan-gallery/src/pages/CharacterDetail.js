import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import StoryViewer from '../components/StoryViewer';
import charactersData from '../data/characters.json';
import './CharacterDetail.css';

function CharacterDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [character, setCharacter] = useState(null);
  const [selectedTheme, setSelectedTheme] = useState(null);

  useEffect(() => {
    // ID로 캐릭터 찾기 (문자열을 숫자로 변환)
    const found = charactersData.find(char => char.id === parseInt(id));

    if (found) {
      setCharacter(found);
      // 첫 번째 테마를 기본 선택
      if (found.themes && found.themes.length > 0) {
        setSelectedTheme(found.themes[0]);
      }
    } else {
      // 캐릭터를 찾지 못하면 갤러리로 리다이렉트
      navigate('/');
    }
  }, [id, navigate]);

  if (!character) {
    return (
      <div className="character-detail-loading">
        <p>로딩 중...</p>
      </div>
    );
  }

  // 테마가 없는 경우 처리
  if (!character.themes || character.themes.length === 0) {
    return (
      <div className="character-detail-container">
        <Header />
        <div className="character-detail-content">
          <div className="character-header">
            <button onClick={() => navigate('/')} className="back-button">
              ← 갤러리로 돌아가기
            </button>
            <h1>{character.name}</h1>
            <p className="series-name">{character.series}</p>
          </div>
          <div className="no-themes-message">
            <p>아직 테마가 준비되지 않았습니다.</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="character-detail-container">
      <Header />
      <div className="character-detail-content">
        {/* 캐릭터 헤더 */}
        <div className="character-header">
          <button onClick={() => navigate('/')} className="back-button">
            ← 갤러리로 돌아가기
          </button>
          <h1>{character.name}</h1>
          <p className="series-name">{character.series}</p>
        </div>

        {/* 테마 탭 네비게이션 */}
        <div className="theme-navigation">
          {character.themes.map((theme) => (
            <button
              key={theme.id}
              className={`theme-tab ${selectedTheme?.id === theme.id ? 'active' : ''}`}
              onClick={() => setSelectedTheme(theme)}
            >
              <div className="theme-tab-content">
                <span className="theme-title">{theme.title}</span>
                <span className="theme-description">{theme.description}</span>
              </div>
            </button>
          ))}
        </div>

        {/* 스토리 뷰어 */}
        {selectedTheme && <StoryViewer theme={selectedTheme} />}
      </div>
      <Footer />
    </div>
  );
}

export default CharacterDetail;
