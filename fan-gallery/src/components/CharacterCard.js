import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './CharacterCard.css';

function CharacterCard({ character }) {
  const [imageAspectRatio, setImageAspectRatio] = useState(null);
  const imgRef = useRef(null);

  useEffect(() => {
    const img = imgRef.current;
    if (img && img.complete) {
      // 이미지가 이미 로드된 경우
      const aspectRatio = img.naturalHeight / img.naturalWidth;
      setImageAspectRatio(aspectRatio);
    }
  }, []);

  const handleImageLoad = (e) => {
    const img = e.target;
    if (img.naturalWidth && img.naturalHeight) {
      const aspectRatio = img.naturalHeight / img.naturalWidth;
      setImageAspectRatio(aspectRatio);
    }
  };

  return (
    <Link to={`/character/${character.id}`} className="character-card">
      <div 
        className="character-image-wrapper"
        style={imageAspectRatio ? { paddingTop: `${imageAspectRatio * 100}%` } : {}}
      >
        <img
          ref={imgRef}
          src={character.image}
          alt={character.name}
          className="character-image"
          onLoad={handleImageLoad}
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/300x400?text=' + encodeURIComponent(character.name);
          }}
        />
      </div>
      <div className="character-info">
        <h3 className="character-name">{character.name_kr || character.name}</h3>
        <p className="character-series">{character.series}</p>
      </div>
    </Link>
  );
}

export default CharacterCard;
