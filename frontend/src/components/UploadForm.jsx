import React, { useEffect, useState } from 'react';
import './UploadForm.css';

export default function UploadForm({ onFilesChange, onSubmit }) {
  const [cubeCount, setCubeCount] = useState(0);

  useEffect(() => {
    fetch('http://localhost:5000/cube-count')
      .then(res => res.json())
      .then(data => setCubeCount(data.count))
      .catch(() => setCubeCount(0));
  }, []);

  return (
    <div className="form-container">
      <div className="cube-bubble">
        🎉 We've solved <strong>{cubeCount}</strong> cubes so far!
      </div>

      <div className="form-header">
        <img src="/assets/cube_logo.png" alt="Cube" className="form-logo" />
        <h1 className="form-title">Rubik’s Cube Solver</h1>
      </div>

      <p className="form-instruction">Upload 6 images (1 per face):</p>

      <label htmlFor="file-upload" className="custom-file-upload">
        📁 Choose Images
        <input
          id="file-upload"
          type="file"
          accept="image/*"
          multiple
          onChange={onFilesChange}
        />
      </label>

      <button className="upload-button" onClick={onSubmit}>
        🚀 Upload and Solve
      </button>
    </div>
  );
}
