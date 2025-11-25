import React, { useState, useMemo } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import GalleryGrid from '../components/GalleryGrid';
import charactersData from '../data/characters.json';
import './Gallery.css';

function Gallery() {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredCharacters = useMemo(() => {
    if (!searchTerm.trim()) {
      return charactersData;
    }

    return charactersData.filter((character) => {
      const nameMatch = character.name.toLowerCase().includes(searchTerm.toLowerCase());
      const nameKrMatch = character.name_kr && character.name_kr.includes(searchTerm);
      const seriesMatch = character.series.toLowerCase().includes(searchTerm.toLowerCase());
      return nameMatch || nameKrMatch || seriesMatch;
    });
  }, [searchTerm]);

  return (
    <div className="gallery-page">
      <Header searchTerm={searchTerm} onSearchChange={setSearchTerm} />
      <main className="gallery-main">
        <div className="gallery-header">
          <h2 className="gallery-title">캐릭터 갤러리</h2>
          <p className="gallery-subtitle">
            총 {filteredCharacters.length}명의 캐릭터
          </p>
        </div>
        <GalleryGrid characters={filteredCharacters} />
      </main>
      <Footer />
    </div>
  );
}

export default Gallery;
