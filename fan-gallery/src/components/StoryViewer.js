import React from 'react';
import StoryPanel from './StoryPanel';
import './StoryViewer.css';

function StoryViewer({ theme }) {
  if (!theme || !theme.story || theme.story.length === 0) {
    return (
      <div className="story-viewer-empty">
        <p>스토리가 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="story-viewer">
      <div className="story-header">
        <h2>{theme.title}</h2>
        <p className="story-description">{theme.description}</p>
      </div>

      <div className="story-panels">
        {theme.story.map((panel, index) => (
          <StoryPanel
            key={index}
            image={panel.image}
            narration={panel.narration}
            index={index}
          />
        ))}
      </div>
    </div>
  );
}

export default StoryViewer;
