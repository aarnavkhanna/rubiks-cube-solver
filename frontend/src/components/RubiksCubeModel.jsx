import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';

const faceColor = (face, pos) => {
  if (face === 0 && pos[0] === 1) return 'green';   // +X → right
  if (face === 1 && pos[0] === -1) return 'blue';   // -X → left
  if (face === 2 && pos[1] === 1) return 'white';   // +Y → top
  if (face === 3 && pos[1] === -1) return 'yellow'; // -Y → bottom
  if (face === 4 && pos[2] === 1) return 'red';     // +Z → front
  if (face === 5 && pos[2] === -1) return 'orange'; // -Z → back
  return '#111'; // hidden faces
};

export default function RubiksCubeModel() {
  const cubeRef = useRef();

  useFrame(() => {
    if (cubeRef.current) {
      cubeRef.current.rotation.y += 0.002;
    }
  });

  return (
    <group ref={cubeRef}>
      {[-1, 0, 1].flatMap((x) =>
        [-1, 0, 1].flatMap((y) =>
          [-1, 0, 1].map((z) => {
            const position = [x, y, z];
            const materials = Array(6)
              .fill()
              .map((_, faceIndex) => (
                <meshStandardMaterial
                  key={faceIndex}
                  attachArray="material"
                  color={faceColor(faceIndex, position)}
                />
              ));

            return (
              <mesh
                key={`${x}${y}${z}`}
                position={[x * 1.05, y * 1.05, z * 1.05]}
                castShadow
                receiveShadow
              >
                <boxGeometry args={[1, 1, 1]} />
                {materials}
              </mesh>
            );
          })
        )
      )}
    </group>
  );
}
