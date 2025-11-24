import React, { useMemo } from 'react';
import StoryPanel from './StoryPanel';
import imagesData from '../data/images.json';
import './StoryViewer.css';

const R2_DOMAIN = 'https://animetoast.zowoo.uk';

function StoryViewer({ theme, characterName }) {
  // pose 테마일 때 images.json에서 이미지 리스트 가져오기
  const storyPanels = useMemo(() => {
    if (!theme) return [];

    // 기존 story가 있으면 사용
    if (theme.story && theme.story.length > 0) {
      return theme.story;
    }

    // pose 테마이고 images.json에 데이터가 있으면 동적으로 생성
    if (theme.id === 'pose' && characterName && imagesData.character && imagesData.character[characterName]) {
      const characterImages = imagesData.character[characterName];
      if (characterImages.pose && Array.isArray(characterImages.pose)) {
        return characterImages.pose.map((imagePath, index) => ({
          image: `${R2_DOMAIN}/${imagePath}`,
          narration: `${index + 1}번째 이미지`,
          index: index
        }));
      }
    }

    return [];
  }, [theme, characterName]);

  if (!theme || storyPanels.length === 0) {
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
        {storyPanels.map((panel, index) => (
          <StoryPanel
            key={index}
            image={panel.image}
            narration={panel.narration || ''}
            index={index}
          />
        ))}
      </div>
    </div>
  );
}

export default StoryViewer;
