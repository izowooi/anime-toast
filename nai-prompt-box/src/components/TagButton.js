import React from 'react';
import './TagButton.css';

function TagButton({ label, tag, onCopy }) {
  const handleClick = async () => {
    try {
      await navigator.clipboard.writeText(tag);
      onCopy(`${label} 복사됨`);
    } catch (err) {
      console.error('복사 실패:', err);
      onCopy('복사 실패');
    }
  };

  return (
    <button className="tag-button" onClick={handleClick}>
      <span className="tag-button-icon">📋</span>
      <span className="tag-button-label">{label}</span>
    </button>
  );
}

export default TagButton;

