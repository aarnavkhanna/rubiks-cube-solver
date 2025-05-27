// LoadingScreen.jsx
import React, { useEffect, useState } from 'react';
import './LoadingScreen.css';

export default function LoadingScreen({ onFinish }) {
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setFadeOut(true);
      setTimeout(onFinish, 800);
    }, 2500);

    return () => clearTimeout(timer);
  }, [onFinish]);

  return (
    <div className={`loading-screen ${fadeOut ? 'fade-out' : ''}`}>
      <img
        src="/assets/cube_logo.png"
        alt="Rubik’s Cube Logo"
        className="cube-logo"
      />
    </div>
  );
}

