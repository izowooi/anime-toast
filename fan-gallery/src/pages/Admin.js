import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import ImageUploader from '../components/admin/ImageUploader';
import * as api from '../services/api';
import './Admin.css';

function Admin() {
  const navigate = useNavigate();
  const [characters, setCharacters] = useState([]);
  const [selectedCharacter, setSelectedCharacter] = useState(null);
  const [selectedTheme, setSelectedTheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState(null);

  // 폼 상태
  const [characterForm, setCharacterForm] = useState({ name: '', series: '', image_url: '' });
  const [themeForm, setThemeForm] = useState({ theme_id: '', title: '', description: '', cover_image_url: '', sort_order: 0 });
  const [panelForm, setPanelForm] = useState({ image_url: '', narration: '', sort_order: 0 });

  useEffect(() => {
    loadCharacters();
  }, []);

  const loadCharacters = async () => {
    try {
      setLoading(true);
      const data = await api.getAllCharacters();
      setCharacters(data || []);
    } catch (error) {
      showMessage('캐릭터 로딩 실패: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (msg, type = 'success') => {
    setMessage({ text: msg, type });
    setTimeout(() => setMessage(null), 3000);
  };

  // ============= 캐릭터 CRUD =============

  const handleCreateCharacter = async (e) => {
    e.preventDefault();
    try {
      await api.createCharacter(characterForm);
      showMessage('캐릭터가 추가되었습니다.');
      setCharacterForm({ name: '', series: '', image_url: '' });
      await loadCharacters();
    } catch (error) {
      showMessage('캐릭터 추가 실패: ' + error.message, 'error');
    }
  };

  const handleDeleteCharacter = async (id) => {
    if (!window.confirm('정말 삭제하시겠습니까?')) return;
    try {
      await api.deleteCharacter(id);
      showMessage('캐릭터가 삭제되었습니다.');
      await loadCharacters();
      if (selectedCharacter?.id === id) {
        setSelectedCharacter(null);
      }
    } catch (error) {
      showMessage('캐릭터 삭제 실패: ' + error.message, 'error');
    }
  };

  // ============= 테마 CRUD =============

  const handleSelectCharacter = async (character) => {
    setSelectedCharacter(character);
    setSelectedTheme(null);
    try {
      const fullData = await api.getCharacterById(character.id);
      setSelectedCharacter(fullData);
    } catch (error) {
      showMessage('캐릭터 상세 로딩 실패: ' + error.message, 'error');
    }
  };

  const handleCreateTheme = async (e) => {
    e.preventDefault();
    if (!selectedCharacter) {
      showMessage('캐릭터를 먼저 선택해주세요.', 'error');
      return;
    }
    try {
      await api.createTheme({
        ...themeForm,
        character_id: selectedCharacter.id,
      });
      showMessage('테마가 추가되었습니다.');
      setThemeForm({ theme_id: '', title: '', description: '', cover_image_url: '', sort_order: 0 });
      await handleSelectCharacter(selectedCharacter);
    } catch (error) {
      showMessage('테마 추가 실패: ' + error.message, 'error');
    }
  };

  const handleDeleteTheme = async (id) => {
    if (!window.confirm('정말 삭제하시겠습니까?')) return;
    try {
      await api.deleteTheme(id);
      showMessage('테마가 삭제되었습니다.');
      await handleSelectCharacter(selectedCharacter);
      if (selectedTheme?.id === id) {
        setSelectedTheme(null);
      }
    } catch (error) {
      showMessage('테마 삭제 실패: ' + error.message, 'error');
    }
  };

  // ============= 스토리 패널 CRUD =============

  const handleSelectTheme = (theme) => {
    setSelectedTheme(theme);
  };

  const handleCreatePanel = async (e) => {
    e.preventDefault();
    if (!selectedTheme) {
      showMessage('테마를 먼저 선택해주세요.', 'error');
      return;
    }
    try {
      await api.createStoryPanel({
        ...panelForm,
        theme_id: selectedTheme.id,
      });
      showMessage('스토리 패널이 추가되었습니다.');
      setPanelForm({ image_url: '', narration: '', sort_order: 0 });
      await handleSelectCharacter(selectedCharacter);
      // 선택된 테마 업데이트
      const updatedTheme = selectedCharacter.themes.find(t => t.id === selectedTheme.id);
      setSelectedTheme(updatedTheme);
    } catch (error) {
      showMessage('스토리 패널 추가 실패: ' + error.message, 'error');
    }
  };

  const handleDeletePanel = async (id) => {
    if (!window.confirm('정말 삭제하시겠습니까?')) return;
    try {
      await api.deleteStoryPanel(id);
      showMessage('스토리 패널이 삭제되었습니다.');
      await handleSelectCharacter(selectedCharacter);
      const updatedTheme = selectedCharacter.themes.find(t => t.id === selectedTheme.id);
      setSelectedTheme(updatedTheme);
    } catch (error) {
      showMessage('스토리 패널 삭제 실패: ' + error.message, 'error');
    }
  };

  if (loading) {
    return <div className="admin-loading">로딩 중...</div>;
  }

  return (
    <div className="admin-container">
      <Header />
      <div className="admin-content">
        <div className="admin-header">
          <h1>관리자 페이지</h1>
          <button onClick={() => navigate('/')} className="back-button">
            갤러리로 돌아가기
          </button>
        </div>

        {message && (
          <div className={`message ${message.type}`}>
            {message.text}
          </div>
        )}

        <div className="admin-grid">
          {/* 캐릭터 목록 */}
          <div className="admin-section">
            <h2>캐릭터 관리</h2>
            <form onSubmit={handleCreateCharacter} className="admin-form">
              <input
                type="text"
                placeholder="캐릭터 이름"
                value={characterForm.name}
                onChange={(e) => setCharacterForm({...characterForm, name: e.target.value})}
                required
              />
              <input
                type="text"
                placeholder="시리즈"
                value={characterForm.series}
                onChange={(e) => setCharacterForm({...characterForm, series: e.target.value})}
                required
              />
              <input
                type="text"
                placeholder="이미지 URL"
                value={characterForm.image_url}
                onChange={(e) => setCharacterForm({...characterForm, image_url: e.target.value})}
                required
              />
              <ImageUploader
                folder="characters"
                onUploadSuccess={(url) => setCharacterForm({...characterForm, image_url: url})}
              />
              <button type="submit" className="btn-primary">캐릭터 추가</button>
            </form>

            <div className="item-list">
              {characters.map((char) => (
                <div key={char.id} className={`item ${selectedCharacter?.id === char.id ? 'active' : ''}`}>
                  <div onClick={() => handleSelectCharacter(char)} className="item-info">
                    <img src={char.image_url} alt={char.name} className="thumbnail" />
                    <div>
                      <strong>{char.name}</strong>
                      <p>{char.series}</p>
                    </div>
                  </div>
                  <button onClick={() => handleDeleteCharacter(char.id)} className="btn-danger">삭제</button>
                </div>
              ))}
            </div>
          </div>

          {/* 테마 관리 */}
          {selectedCharacter && (
            <div className="admin-section">
              <h2>{selectedCharacter.name}의 테마</h2>
              <form onSubmit={handleCreateTheme} className="admin-form">
                <input
                  type="text"
                  placeholder="테마 ID (예: beach)"
                  value={themeForm.theme_id}
                  onChange={(e) => setThemeForm({...themeForm, theme_id: e.target.value})}
                  required
                />
                <input
                  type="text"
                  placeholder="제목"
                  value={themeForm.title}
                  onChange={(e) => setThemeForm({...themeForm, title: e.target.value})}
                  required
                />
                <input
                  type="text"
                  placeholder="설명"
                  value={themeForm.description}
                  onChange={(e) => setThemeForm({...themeForm, description: e.target.value})}
                />
                <input
                  type="number"
                  placeholder="순서"
                  value={themeForm.sort_order}
                  onChange={(e) => setThemeForm({...themeForm, sort_order: parseInt(e.target.value)})}
                />
                <input
                  type="text"
                  placeholder="커버 이미지 URL"
                  value={themeForm.cover_image_url}
                  onChange={(e) => setThemeForm({...themeForm, cover_image_url: e.target.value})}
                  required
                />
                <ImageUploader
                  folder={`themes/${selectedCharacter.name}`}
                  onUploadSuccess={(url) => setThemeForm({...themeForm, cover_image_url: url})}
                />
                <button type="submit" className="btn-primary">테마 추가</button>
              </form>

              <div className="item-list">
                {selectedCharacter.themes?.map((theme) => (
                  <div key={theme.id} className={`item ${selectedTheme?.id === theme.id ? 'active' : ''}`}>
                    <div onClick={() => handleSelectTheme(theme)} className="item-info">
                      <img src={theme.cover_image_url} alt={theme.title} className="thumbnail" />
                      <div>
                        <strong>{theme.title}</strong>
                        <p>{theme.description}</p>
                      </div>
                    </div>
                    <button onClick={() => handleDeleteTheme(theme.id)} className="btn-danger">삭제</button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 스토리 패널 관리 */}
          {selectedTheme && (
            <div className="admin-section">
              <h2>{selectedTheme.title} 스토리 패널</h2>
              <form onSubmit={handleCreatePanel} className="admin-form">
                <input
                  type="text"
                  placeholder="이미지 URL"
                  value={panelForm.image_url}
                  onChange={(e) => setPanelForm({...panelForm, image_url: e.target.value})}
                  required
                />
                <ImageUploader
                  folder={`panels/${selectedCharacter.name}/${selectedTheme.theme_id}`}
                  onUploadSuccess={(url) => setPanelForm({...panelForm, image_url: url})}
                />
                <textarea
                  placeholder="나레이션"
                  value={panelForm.narration}
                  onChange={(e) => setPanelForm({...panelForm, narration: e.target.value})}
                  required
                  rows="3"
                />
                <input
                  type="number"
                  placeholder="순서"
                  value={panelForm.sort_order}
                  onChange={(e) => setPanelForm({...panelForm, sort_order: parseInt(e.target.value)})}
                />
                <button type="submit" className="btn-primary">패널 추가</button>
              </form>

              <div className="item-list">
                {selectedTheme.story_panels?.map((panel) => (
                  <div key={panel.id} className="item panel-item">
                    <div className="item-info">
                      <img src={panel.image_url} alt={`Panel ${panel.sort_order}`} className="thumbnail" />
                      <div>
                        <strong>순서: {panel.sort_order}</strong>
                        <p>{panel.narration.substring(0, 50)}...</p>
                      </div>
                    </div>
                    <button onClick={() => handleDeletePanel(panel.id)} className="btn-danger">삭제</button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Admin;
