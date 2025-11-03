import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import CategorySection from './components/CategorySection';
import Toast from './components/Toast';
import { artTags, poseTags, categoryConfig } from './data/tags';

function App() {
  const [toastMessage, setToastMessage] = useState('');
  const [isToastVisible, setIsToastVisible] = useState(false);

  const handleCopy = (message) => {
    setToastMessage(message);
    setIsToastVisible(true);
  };

  const handleToastClose = () => {
    setIsToastVisible(false);
  };

  return (
    <div className="App">
      <Header />
      <main className="app-main">
        <div className="app-content">
          <CategorySection
            categoryName={categoryConfig.art.name}
            tags={artTags}
            onCopy={handleCopy}
            wildcardEnabled={categoryConfig.art.wildcardEnabled}
          />
          <CategorySection
            categoryName={categoryConfig.pose.name}
            tags={poseTags}
            onCopy={handleCopy}
            wildcardEnabled={categoryConfig.pose.wildcardEnabled}
          />
        </div>
      </main>
      <Toast
        message={toastMessage}
        isVisible={isToastVisible}
        onClose={handleToastClose}
      />
    </div>
  );
}

export default App;
