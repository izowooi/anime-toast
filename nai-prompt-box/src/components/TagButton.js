import React from 'react';
import './TagButton.css';

function TagButton({ label, tag, onCopy, mode = 'single', selected = false, onToggle }) {
  const handleClick = async () => {
    if (mode === 'multi') {
      // Multi mode: toggle selection
      onToggle();
    } else {
      // Single mode: copy to clipboard
      try {
        await navigator.clipboard.writeText(tag);
        onCopy(`${label} 복사됨`);
      } catch (err) {
        console.error('복사 실패:', err);
        onCopy('복사 실패');
      }
    }
  };

  return (
    <button
      className={`tag-button ${mode === 'multi' ? 'multi-mode' : ''} ${selected ? 'selected' : ''}`}
      onClick={handleClick}
    >
      {mode === 'multi' && (
        <span className="tag-button-checkbox">
          {selected ? '☑' : '☐'}
        </span>
      )}
      <span className="tag-button-icon">📋</span>
      <span className="tag-button-label">{label}</span>
    </button>
  );
}

export default TagButton;

