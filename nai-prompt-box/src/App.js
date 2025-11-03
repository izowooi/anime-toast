import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import CategorySection from './components/CategorySection';
import Toast from './components/Toast';
import { artTags, poseTags } from './data/tags';

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
            categoryName="작화"
            tags={artTags}
            onCopy={handleCopy}
          />
          <CategorySection
            categoryName="포즈"
            tags={poseTags}
            onCopy={handleCopy}
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
