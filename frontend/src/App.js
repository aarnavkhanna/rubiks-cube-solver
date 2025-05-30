import React from 'react';
import InteractiveCube from './components/InteractiveCube';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Rubik's Cube Solver</h1>
      </header>
      <main style={{ height: '80vh', width: '100%' }}>
        <InteractiveCube />
      </main>
    </div>
  );
}

export default App;