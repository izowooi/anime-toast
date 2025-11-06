import React, { useState, useMemo } from 'react';
import { allSeries, charactersBySeriesMap } from '../data/tags';
import './SeriesFilter.css';

const SeriesFilter = ({ onSeriesChange, onViewModeChange }) => {
  const [viewMode, setViewMode] = useState('all'); // 'all' or 'bySeries'
  const [selectedSeries, setSelectedSeries] = useState(null);

  // 작품명을 한국어 이름으로 매핑
  const seriesKoMap = useMemo(() => {
    const map = {};
    Object.entries(charactersBySeriesMap).forEach(([series, characters]) => {
      if (characters.length > 0 && characters[0].series_ko) {
        map[series] = characters[0].series_ko;
      } else {
        map[series] = series;
      }
    });
    return map;
  }, []);

  const handleViewModeToggle = (newMode) => {
    setViewMode(newMode);
    onViewModeChange(newMode);

    // 모드 변경 시 필터 초기화
    if (newMode === 'all') {
      setSelectedSeries(null);
      onSeriesChange(null);
    }
  };

  const handleSeriesClick = (series) => {
    const isSelected = selectedSeries === series;
    const newSeries = isSelected ? null : series;
    setSelectedSeries(newSeries);
    onSeriesChange(newSeries);
  };

  return (
    <div className="series-filter">
      <div className="filter-mode-toggle">
        <button
          className={`toggle-button ${viewMode === 'all' ? 'active' : ''}`}
          onClick={() => handleViewModeToggle('all')}
          title="모든 캐릭터 표시"
        >
          📋 전체 보기
        </button>
        <button
          className={`toggle-button ${viewMode === 'bySeries' ? 'active' : ''}`}
          onClick={() => handleViewModeToggle('bySeries')}
          title="작품별로 필터링"
        >
          🎬 작품별 보기
        </button>
      </div>

      {viewMode === 'bySeries' && (
        <div className="series-tabs">
          {allSeries.map((series) => {
            const seriesKoName = seriesKoMap[series] || series;
            const displayName = seriesKoName.length > 15 ? `${seriesKoName.substring(0, 12)}...` : seriesKoName;
            return (
              <button
                key={series}
                className={`series-tab ${selectedSeries === series ? 'active' : ''}`}
                onClick={() => handleSeriesClick(series)}
                title={seriesKoName}
              >
                {displayName}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default SeriesFilter;
