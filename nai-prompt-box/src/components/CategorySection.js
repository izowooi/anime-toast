import React, { useState } from 'react';
import TagButton from './TagButton';
import './CategorySection.css';

function CategorySection({ categoryName, tags, onCopy, wildcardEnabled = false }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [mode, setMode] = useState('single'); // 'single' or 'multi'
  const [selectedTags, setSelectedTags] = useState([]);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const handleModeChange = (newMode) => {
    setMode(newMode);
    if (newMode === 'single') {
      setSelectedTags([]); // Clear selections when switching to single mode
    }
  };

  const handleTagToggle = (label, tag) => {
    if (mode === 'single') {
      // Single mode: copy immediately
      return;
    }

    // Multi mode: toggle selection
    setSelectedTags(prev => {
      if (prev.some(item => item.label === label)) {
        return prev.filter(item => item.label !== label);
      } else {
        return [...prev, { label, tag }];
      }
    });
  };

  const handleWildcardCopy = async () => {
    if (selectedTags.length === 0) return;

    const wildcardString = `||${selectedTags.map(item => item.tag).join('|')}||`;
    try {
      await navigator.clipboard.writeText(wildcardString);
      onCopy(`와일드카드 복사됨 (${selectedTags.length}개)`);
      setSelectedTags([]); // Clear selections after copy
    } catch (err) {
      console.error('복사 실패:', err);
      onCopy('복사 실패');
    }
  };

  return (
    <div className="category-section">
      <button className="category-header" onClick={toggleExpand}>
        <span className="category-name">{categoryName}</span>
        <span className="category-icon">{isExpanded ? '▼' : '▶'}</span>
      </button>
      {isExpanded && (
        <>
          {wildcardEnabled && (
            <div className="mode-toggle">
              <button
                className={`mode-button ${mode === 'single' ? 'active' : ''}`}
                onClick={() => handleModeChange('single')}
              >
                Single
              </button>
              <button
                className={`mode-button ${mode === 'multi' ? 'active' : ''}`}
                onClick={() => handleModeChange('multi')}
              >
                Multi {mode === 'multi' && `(${selectedTags.length}/${Object.keys(tags).length})`}
              </button>
            </div>
          )}
          <div className="category-content">
            {Object.entries(tags).map(([label, tag]) => (
              <TagButton
                key={label}
                label={label}
                tag={tag}
                mode={mode}
                selected={selectedTags.some(item => item.label === label)}
                onCopy={onCopy}
                onToggle={() => handleTagToggle(label, tag)}
              />
            ))}
          </div>
          {mode === 'multi' && selectedTags.length > 0 && (
            <div className="wildcard-copy-container">
              <button className="wildcard-copy-button" onClick={handleWildcardCopy}>
                📋 Copy Wildcard ({selectedTags.length})
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default CategorySection;

