import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import CubeCanvas from './components/CubeCanvas';
import LoadingScreen from './components/LoadingScreen';
import './App.css'; // 🟣 Add this line to use the global styles

function App() {
  const [showMain, setShowMain] = useState(false);

  const handleFileChange = () => {};
  const handleSubmit = () => {};

  return (
    <div className="app-wrapper">
      {!showMain && <LoadingScreen onFinish={() => setShowMain(true)} />}
      {showMain && (
        <div className="main-container">
          <UploadForm onFilesChange={handleFileChange} onSubmit={handleSubmit} />
          <div className="cube-area">
            <CubeCanvas />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
