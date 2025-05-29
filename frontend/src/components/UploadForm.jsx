import React, { useEffect, useState } from 'react';
import './UploadForm.css';

export default function UploadForm() {
  const [cubeCount, setCubeCount] = useState(0);
  const [images, setImages] = useState({});
  const [loading, setLoading] = useState(false);
  const [solution, setSolution] = useState('');

  useEffect(() => {
    fetch('http://localhost:5000/cube-count')
      .then(res => res.json())
      .then(data => setCubeCount(data.count))
      .catch(() => setCubeCount(0));
  }, []);

  const handleFilesChange = (e) => {
    const files = e.target.files;
    const imageMap = {};
    for (let i = 0; i < files.length && i < 6; i++) {
      imageMap[`face${i + 1}`] = files[i];
    }
    setImages(imageMap);
  };

  const handleSubmit = async () => {
    if (Object.keys(images).length !== 6) {
      alert('Please upload exactly 6 images (one per cube face)');
      return;
    }

    const formData = new FormData();
    for (let i = 1; i <= 6; i++) {
      formData.append(`face${i}`, images[`face${i}`]);
    }

    try {
      setLoading(true);
      const res = await fetch('http://localhost:5000/upload-images', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      setLoading(false);

      if (res.ok) {
        setSolution(data.solution);
      } else {
        setSolution('❌ ' + (data.message || data.error));
      }
    } catch (err) {
      setLoading(false);
      setSolution('❌ Upload failed. Check backend or try again.');
      console.error(err);
    }
  };

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
          onChange={handleFilesChange}
        />
      </label>

      <button className="upload-button" onClick={handleSubmit} disabled={loading}>
        🚀 {loading ? 'Solving...' : 'Upload and Solve'}
      </button>

      {loading && <div className="loading-bar"><div className="loading-fill" /></div>}

      {solution && (
        <div className="solution-box">
          🧩 <strong>Solution:</strong> {solution}
        </div>
      )}
    </div>
  );
}
