import React, { Suspense, useRef, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import { useGLTF, useAnimations } from '@react-three/drei';
import * as THREE from 'three';

export default function RubikModel() {
  const group = useRef();
  const { scene, animations } = useGLTF('/models/rubiks_cube.glb');
  const { actions } = useAnimations(animations, group);

  useEffect(() => {
    // Play animation if available
    if (actions && animations.length > 0) {
      const action = actions[animations[0].name];
      action.play();
    }
  }, [actions, animations]);

  useFrame(() => {
    if (group.current) {
      group.current.rotation.y += 0.002;
    }
  });

  // Shift model left a bit
  useEffect(() => {
    const box = new THREE.Box3().setFromObject(scene);
    const center = new THREE.Vector3();
    box.getCenter(center);
    scene.position.sub(center); // First center it

    // Then nudge it slightly left on the X-axis
    scene.position.x -= 0.5; // adjust this value if needed
  }, [scene]);

  return (
    <Suspense fallback={null}>
      <primitive object={scene} ref={group} scale={1.5} />
    </Suspense>
  );
}
