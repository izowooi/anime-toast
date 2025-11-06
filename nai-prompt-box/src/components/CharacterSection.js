import React, { useState, useMemo } from 'react';
import { charactersBySeriesMap, allSeries } from '../data/tags';
import { searchCharacters, groupCharactersBySeriesName, getAllCharacters } from '../utils/searchCharacters';
import CharacterSearch from './CharacterSearch';
import SeriesFilter from './SeriesFilter';
import TagButton from './TagButton';
import './CharacterSection.css';

const CharacterSection = ({ onTagCopy }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [viewMode, setViewMode] = useState('all');
  const [selectedSeries, setSelectedSeries] = useState(null);

  const handleCopy = (message) => {
    onTagCopy(message);
  };

  // 필터링된 캐릭터 계산
  const filteredCharacters = useMemo(() => {
    const baseCharacters = searchCharacters(searchQuery, selectedSeries);
    return baseCharacters;
  }, [searchQuery, selectedSeries]);

  // 작품별로 그룹화된 캐릭터
  const charactersBySeriesGrouped = useMemo(() => {
    return groupCharactersBySeriesName(filteredCharacters);
  }, [filteredCharacters]);

  const totalCharacterCount = useMemo(() => {
    return getAllCharacters().length;
  }, []);

  const handleSearch = (query) => {
    setSearchQuery(query);
  };

  const handleSeriesChange = (series) => {
    setSelectedSeries(series);
  };

  const handleViewModeChange = (newMode) => {
    setViewMode(newMode);
  };

  // 캐릭터를 렌더링할 때 작품별로 그룹화할지 여부
  const shouldGroupBySeriesDisplay = viewMode === 'bySeries' || (viewMode === 'all' && selectedSeries === null);

  return (
    <div className="category-section character-section">
      <div
        className="category-header"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <span className="category-title">캐릭터</span>
        <span className="expand-icon">{isExpanded ? '▼' : '▶'}</span>
      </div>

      {isExpanded && (
        <div className="category-content">
          <CharacterSearch
            onSearch={handleSearch}
            totalCount={totalCharacterCount}
            resultCount={filteredCharacters.length}
          />

          <SeriesFilter
            onSeriesChange={handleSeriesChange}
            onViewModeChange={handleViewModeChange}
          />

          <div className="characters-container">
            {shouldGroupBySeriesDisplay ? (
              // 작품별 그룹화 표시
              Object.entries(charactersBySeriesGrouped)
                .sort(([seriesA], [seriesB]) => seriesA.localeCompare(seriesB))
                .map(([series, characters]) => {
                  // 현재 작품의 한국어 이름 찾기
                  const seriesKoName = characters[0]?.series_ko || series;
                  return (
                    <div key={series} className="series-group">
                      <div className="series-name">{seriesKoName}</div>
                      <div className="characters-grid">
                        {characters.map((char) => (
                          <TagButton
                            key={char.id}
                            label={char.name_ko || char.name}
                            tag={char.tag}
                            mode="single"
                            selected={false}
                            onCopy={handleCopy}
                            onToggle={() => {}}
                          />
                        ))}
                      </div>
                    </div>
                  );
                })
            ) : (
              // 단순 리스트 표시 (검색 결과)
              <div className="characters-grid">
                {filteredCharacters.map((char) => (
                  <TagButton
                    key={char.id}
                    label={char.name_ko || char.name}
                    tag={char.tag}
                    mode="single"
                    selected={false}
                    onCopy={handleCopy}
                    onToggle={() => {}}
                  />
                ))}
              </div>
            )}

            {filteredCharacters.length === 0 && (
              <div className="no-results">
                검색 결과가 없습니다.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CharacterSection;
