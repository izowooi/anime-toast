import React, { useState } from 'react';
import './CharacterSearch.css';

const CharacterSearch = ({ onSearch, totalCount, resultCount }) => {
  const [searchQuery, setSearchQuery] = useState('');

  const handleInputChange = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    onSearch(query);
  };

  const handleClear = () => {
    setSearchQuery('');
    onSearch('');
  };

  return (
    <div className="character-search">
      <input
        type="text"
        placeholder="캐릭터명 검색... (예: rem, sailor moon)"
        value={searchQuery}
        onChange={handleInputChange}
        className="search-input"
      />
      {searchQuery && (
        <button
          onClick={handleClear}
          className="clear-button"
          title="검색 초기화"
        >
          ✕
        </button>
      )}
      <span className="search-result-count">
        {resultCount}/{totalCount}
      </span>
    </div>
  );
};

export default CharacterSearch;
