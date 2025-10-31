import React, { useState } from 'react';
import TagButton from './TagButton';
import './CategorySection.css';

function CategorySection({ categoryName, tags, onCopy }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="category-section">
      <button className="category-header" onClick={toggleExpand}>
        <span className="category-name">{categoryName}</span>
        <span className="category-icon">{isExpanded ? '▼' : '▶'}</span>
      </button>
      {isExpanded && (
        <div className="category-content">
          {Object.entries(tags).map(([label, tag]) => (
            <TagButton
              key={label}
              label={label}
              tag={tag}
              onCopy={onCopy}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default CategorySection;

