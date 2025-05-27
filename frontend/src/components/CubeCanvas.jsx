// CubeCanvas.jsx
import React from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import RubikModel from './RubikModel';

export default function CubeCanvas() {
  return (
    <Canvas
      shadows
      camera={{ position: [8, 6, 8], fov: 40 }} // pulled back, lower FOV
      style={{ width: '100%', height: '100%' }}
    >
      <ambientLight intensity={0.9} />
      <directionalLight position={[10, 10, 10]} intensity={1.5} castShadow />
      <RubikModel />
      <OrbitControls enablePan={false} enableZoom={true} />
    </Canvas>
  );
}
