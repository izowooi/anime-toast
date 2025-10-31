import React, { useEffect } from 'react';
import './Toast.css';

function Toast({ message, isVisible, onClose }) {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        onClose();
      }, 2500);
      return () => clearTimeout(timer);
    }
  }, [isVisible, onClose]);

  if (!isVisible) return null;

  return (
    <div className="toast">
      <span className="toast-message">{message}</span>
    </div>
  );
}

export default Toast;

