import React from 'react';
import { Link } from 'react-router-dom';
import './CharacterCard.css';

function CharacterCard({ character }) {
  return (
    <Link to={`/character/${character.id}`} className="character-card">
      <div className="character-image-wrapper">
        <img
          src={character.image}
          alt={character.name}
          className="character-image"
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/300x400?text=' + encodeURIComponent(character.name);
          }}
        />
      </div>
      <div className="character-info">
        <h3 className="character-name">{character.name}</h3>
        <p className="character-series">{character.series}</p>
      </div>
    </Link>
  );
}

export default CharacterCard;
