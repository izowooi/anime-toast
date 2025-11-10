import React, { useState } from 'react';
import './StoryPanel.css';

function StoryPanel({ image, narration, index }) {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  const handleImageError = () => {
    setImageError(true);
  };

  return (
    <div className="story-panel">
      <div className="story-panel-image-container">
        {!imageLoaded && !imageError && (
          <div className="story-panel-loading">이미지 로딩 중...</div>
        )}
        {imageError ? (
          <div className="story-panel-error">이미지를 불러올 수 없습니다</div>
        ) : (
          <img
            src={image}
            alt={`Story panel ${index + 1}`}
            className={`story-panel-image ${imageLoaded ? 'loaded' : ''}`}
            onLoad={handleImageLoad}
            onError={handleImageError}
          />
        )}
      </div>

      <div className="story-panel-narration">
        <div className="narration-content">
          <span className="narration-index">{index + 1}</span>
          <p className="narration-text">{narration}</p>
        </div>
      </div>
    </div>
  );
}

export default StoryPanel;
