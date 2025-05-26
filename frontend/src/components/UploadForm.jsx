import React, { useState } from 'react';
import axios from 'axios';

function UploadForm() {
  const [videoFile, setVideoFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setVideoFile(e.target.files[0]);
    setResponse(null);
    setError(null);
  };

  const handleUpload = async () => {
    if (!videoFile) {
      setError("Please select a video file first.");
      return;
    }

    const formData = new FormData();
    formData.append("video", videoFile);

    try {
      setLoading(true);
      setError(null);

      const res = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });

      setResponse(res.data);
    } catch (err) {
      console.error("Upload failed:", err);
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else {
        setError("Upload failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "1rem", fontFamily: "Arial" }}>
      <h2>Upload a Rubik’s Cube Video</h2>

      <input type="file" accept="video/*" onChange={handleFileChange} />
      <br /><br />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Upload and Solve"}
      </button>

      <br /><br />
      {error && <p style={{ color: "red" }}>❌ {error}</p>}

      {response && (
        <div style={{ marginTop: "1rem" }}>
          <h3>✅ Cube Processed</h3>

          <p><strong>Cube State (raw):</strong></p>
          <code style={{ whiteSpace: "pre-wrap" }}>{response.cube_state}</code>

          <br /><br />
          <p><strong>Advanced Solution (for cubers):</strong></p>
          <code style={{ whiteSpace: "pre-wrap" }}>{response.solution}</code>
        </div>
      )}
    </div>
  );
}

export default UploadForm;
