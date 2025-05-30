import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import CubeModel from './CubeModel';

export default function InteractiveCube() {
  // Initialize a 6-face × 3 rows × 3 cols cubeState of all-black stickers:
  const defaultState = Array.from({ length: 6 }, () =>
    Array.from({ length: 3 }, () =>
      Array.from({ length: 3 }, () => '#000000')
    )
  );

  const [cubeState, setCubeState] = useState(defaultState);
  const [selected, setSelected] = useState(null);

  const handleStickerClick = (face, row, col) => {
    setSelected({ face, row, col });
  };

  const handleColorPick = color => {
    const next = cubeState.map(face =>
      face.map(row => row.slice())
    );
    next[selected.face][selected.row][selected.col] = color;
    setCubeState(next);
    setSelected(null);
  };

  return (
    <div className="cube-area">
      <Canvas
        shadows
        camera={{ position: [5, 5, 5], fov: 50 }}
        gl={{ antialias: true, physicallyCorrectLights: true }}
        style={{ background: '#1e1e1e' }}
      >
        <Environment preset="studio" background={false} />
        <hemisphereLight skyColor="#ffffff" groundColor="#222222" intensity={0.4} />
        <directionalLight
          position={[10, 10, 10]}
          intensity={1.0}
          castShadow
          shadow-mapSize-width={1024}
          shadow-mapSize-height={1024}
        />
        <pointLight position={[-10, 5, -10]} intensity={0.6} />
        <spotLight position={[0, 8, 0]} angle={0.3} penumbra={1} intensity={0.3} castShadow />

        <CubeModel cubeState={cubeState} onStickerClick={handleStickerClick} />

        <OrbitControls enableZoom enablePan enableRotate />
      </Canvas>

      {selected && (
        <div className="palette">
          {['white', 'green', 'red', 'orange', 'blue', 'yellow'].map(c => (
            <button
              key={c}
              style={{
                background: c,
                width: 30,
                height: 30,
                margin: 4,
                border: '1px solid #fff',
                cursor: 'pointer'
              }}
              onClick={() => handleColorPick(c)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
