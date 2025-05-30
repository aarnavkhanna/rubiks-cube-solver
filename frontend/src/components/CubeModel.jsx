// src/components/CubeModel.jsx

import React, { useMemo } from 'react';
import { BoxGeometry, MeshStandardMaterial } from 'three';

export default function CubeModel({ cubeState, onStickerClick }) {
  // size of each mini-cube, with a tiny gap so you see the separations
  const size = 0.98;
  const spacing = 1.02;
  const coords = [-1, 0, 1];

  // define how BoxGeometry’s 6 material slots map to our cubeState faces
  const faceDefs = useMemo(() => [
    // three.js Box face order: 0=right,1=left,2=top,3=bottom,4=front,5=back
    { faceIdx: 0, fIdx: 1, coord: 'x', coordVal:  1, getRowCol: (x,y,z) => [1 - y,   z + 1] }, // Right
    { faceIdx: 1, fIdx: 3, coord: 'x', coordVal: -1, getRowCol: (x,y,z) => [1 - y, 1 - z] }, // Left
    { faceIdx: 2, fIdx: 0, coord: 'y', coordVal:  1, getRowCol: (x,y,z) => [1 - z,   x + 1] }, // Up
    { faceIdx: 3, fIdx: 5, coord: 'y', coordVal: -1, getRowCol: (x,y,z) => [    z + 1, x + 1] }, // Down
    { faceIdx: 4, fIdx: 2, coord: 'z', coordVal:  1, getRowCol: (x,y,z) => [1 - y, 1 - x] }, // Front
    { faceIdx: 5, fIdx: 4, coord: 'z', coordVal: -1, getRowCol: (x,y,z) => [1 - y,   x + 1] }  // Back
  ], []);

  return (
    <group>
      {coords.map(x =>
        coords.map(y =>
          coords.map(z => {
            // build an array of 6 materials for this mini-cube
            const materials = faceDefs.map(def => {
              // default to black plastic
              let color = '#000000';
              // only color faces that lie on the exterior
              const isFace =
                (def.coord === 'x' && x === def.coordVal) ||
                (def.coord === 'y' && y === def.coordVal) ||
                (def.coord === 'z' && z === def.coordVal);

              if (isFace) {
                const [row, col] = def.getRowCol(x, y, z);
                color = cubeState[def.fIdx][row][col];
              }

              return new MeshStandardMaterial({
                color,
                metalness: 0.3,
                roughness: 0.7
              });
            });

            return (
              <mesh
                key={`${x}-${y}-${z}`}
                geometry={new BoxGeometry(size, size, size)}
                material={materials}
                position={[x * spacing, y * spacing, z * spacing]}
                castShadow
                receiveShadow
                onPointerDown={e => {
                  e.stopPropagation();
                  // determine which cube face was clicked
                  const triIndex = e.faceIndex;              // triangle index
                  const matIndex = Math.floor(triIndex / 2); // maps 2 triangles → 1 face
                  const def = faceDefs.find(d => d.faceIdx === matIndex);
                  if (!def) return;

                  const [row, col] = def.getRowCol(x, y, z);
                  onStickerClick(def.fIdx, row, col);
                }}
              />
            );
          })
        )
      )}
    </group>
  );
}
