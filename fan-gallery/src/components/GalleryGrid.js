import React from 'react';
import CharacterCard from './CharacterCard';
import './GalleryGrid.css';

function GalleryGrid({ characters }) {
  if (characters.length === 0) {
    return (
      <div className="gallery-empty">
        <p>검색 결과가 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="gallery-grid">
      {characters.map((character) => (
        <CharacterCard key={character.id} character={character} />
      ))}
    </div>
  );
}

export default GalleryGrid;
