"use client";

import { Canvas, ThreeEvent, useFrame } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { useMemo, useRef } from "react";
import * as THREE from "three";
import { deterministicJitter, regionCoords } from "@/lib/regions";
import type { AgentResponse, Mode, Persona } from "@/lib/types";

const RADIUS = 2;
const DOT_RADIUS = 2.035;
const DOT_SIZE = 0.038;

function latLonToVec3(lat: number, lon: number, radius: number): THREE.Vector3 {
  const phi = ((90 - lat) * Math.PI) / 180;
  const theta = ((lon + 180) * Math.PI) / 180;
  return new THREE.Vector3(
    -radius * Math.sin(phi) * Math.cos(theta),
    radius * Math.cos(phi),
    radius * Math.sin(phi) * Math.sin(theta),
  );
}

function colorFor(response: AgentResponse | undefined, mode: Mode): THREE.Color {
  if (!response || response.position == null) return new THREE.Color("#5a5240");
  if (mode === "forecast") {
    const p =
      typeof response.position === "number"
        ? Math.max(0, Math.min(1, response.position))
        : 0.5;
    return new THREE.Color().setHSL(p * 0.36, 0.7, 0.6);
  }
  const v = String(response.position).toLowerCase();
  if (v === "positive" || v === "supports") return new THREE.Color("#8fb985");
  if (v === "negative" || v === "objects") return new THREE.Color("#c75050");
  return new THREE.Color("#c8b896");
}

interface DotsProps {
  personas: Persona[];
  responses: Record<string, AgentResponse>;
  mode: Mode;
  onSelect: (id: string) => void;
  selectedId: string | null;
}

function Dots({ personas, responses, mode, onSelect, selectedId }: DotsProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null);

  const positions = useMemo(() => {
    return personas.map((p) => {
      const [lat, lon] = regionCoords(p.demographics.region);
      const dLat = deterministicJitter(p.id, 0) * 8;
      const dLon = deterministicJitter(p.id, 1) * 14;
      return latLonToVec3(lat + dLat, lon + dLon, DOT_RADIUS);
    });
  }, [personas]);

  const tempObject = useMemo(() => new THREE.Object3D(), []);
  const tempColor = useMemo(() => new THREE.Color(), []);

  useFrame(({ clock }) => {
    if (!meshRef.current) return;
    const t = clock.getElapsedTime();
    personas.forEach((p, i) => {
      tempObject.position.copy(positions[i]);
      const isSelected = p.id === selectedId;
      const pulse = isSelected ? 2.4 + Math.sin(t * 4) * 0.25 : 1;
      tempObject.scale.setScalar(pulse);
      tempObject.updateMatrix();
      meshRef.current!.setMatrixAt(i, tempObject.matrix);
      tempColor.copy(colorFor(responses[p.id], mode));
      if (isSelected) tempColor.lerp(new THREE.Color("#faf8f3"), 0.4);
      meshRef.current!.setColorAt(i, tempColor);
    });
    meshRef.current.instanceMatrix.needsUpdate = true;
    if (meshRef.current.instanceColor) {
      meshRef.current.instanceColor.needsUpdate = true;
    }
  });

  const onPointerDown = (e: ThreeEvent<PointerEvent>) => {
    e.stopPropagation();
    if (e.instanceId != null) onSelect(personas[e.instanceId].id);
  };

  if (personas.length === 0) return null;

  return (
    <instancedMesh
      ref={meshRef}
      args={[undefined, undefined, personas.length]}
      onPointerDown={onPointerDown}
    >
      <sphereGeometry args={[DOT_SIZE, 12, 12]} />
      <meshBasicMaterial toneMapped={false} />
    </instancedMesh>
  );
}

function Sphere() {
  return (
    <mesh>
      <sphereGeometry args={[RADIUS, 96, 64]} />
      <meshStandardMaterial
        color="#0e1830"
        roughness={0.85}
        metalness={0.05}
        emissive="#050810"
        emissiveIntensity={0.4}
      />
    </mesh>
  );
}

function Atmosphere() {
  return (
    <>
      <mesh>
        <sphereGeometry args={[RADIUS * 1.04, 96, 64]} />
        <meshBasicMaterial
          color="#7a8aa8"
          transparent
          opacity={0.18}
          side={THREE.BackSide}
        />
      </mesh>
      <mesh>
        <sphereGeometry args={[RADIUS * 1.09, 96, 64]} />
        <meshBasicMaterial
          color="#c8b896"
          transparent
          opacity={0.08}
          side={THREE.BackSide}
        />
      </mesh>
    </>
  );
}

function Graticule() {
  const lines = useMemo(() => {
    const out: THREE.Vector3[][] = [];
    for (let lat = -60; lat <= 60; lat += 15) {
      const ring: THREE.Vector3[] = [];
      for (let lon = -180; lon <= 180; lon += 3) {
        ring.push(latLonToVec3(lat, lon, RADIUS + 0.002));
      }
      out.push(ring);
    }
    for (let lon = -180; lon < 180; lon += 15) {
      const ring: THREE.Vector3[] = [];
      for (let lat = -85; lat <= 85; lat += 3) {
        ring.push(latLonToVec3(lat, lon, RADIUS + 0.002));
      }
      out.push(ring);
    }
    return out;
  }, []);

  const equator = useMemo(() => {
    const ring: THREE.Vector3[] = [];
    for (let lon = -180; lon <= 180; lon += 2) {
      ring.push(latLonToVec3(0, lon, RADIUS + 0.003));
    }
    return ring;
  }, []);

  return (
    <>
      {lines.map((pts, i) => (
        <line key={i}>
          <bufferGeometry>
            <bufferAttribute
              attach="attributes-position"
              args={[new Float32Array(pts.flatMap((p) => [p.x, p.y, p.z])), 3]}
            />
          </bufferGeometry>
          <lineBasicMaterial color="#3a4860" transparent opacity={0.55} />
        </line>
      ))}
      <line>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            args={[new Float32Array(equator.flatMap((p) => [p.x, p.y, p.z])), 3]}
          />
        </bufferGeometry>
        <lineBasicMaterial color="#8a7858" transparent opacity={0.65} />
      </line>
    </>
  );
}

function Stars() {
  const positions = useMemo(() => {
    const count = 240;
    const arr = new Float32Array(count * 3);
    const sizes = new Float32Array(count);
    for (let i = 0; i < count; i++) {
      const phi = Math.acos(2 * Math.random() - 1);
      const theta = Math.random() * Math.PI * 2;
      const r = 9 + Math.random() * 6;
      arr[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      arr[i * 3 + 1] = r * Math.cos(phi);
      arr[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
      sizes[i] = 0.5 + Math.random() * 1.5;
    }
    return { arr, sizes };
  }, []);

  return (
    <points>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          args={[positions.arr, 3]}
        />
      </bufferGeometry>
      <pointsMaterial
        color="#e8e2d4"
        size={0.06}
        sizeAttenuation
        transparent
        opacity={0.75}
        toneMapped={false}
      />
    </points>
  );
}

function AutoRotate({ enabled }: { enabled: boolean }) {
  const ref = useRef<THREE.Group>(null);
  useFrame((_, dt) => {
    if (enabled && ref.current) ref.current.rotation.y += dt * 0.03;
  });
  return (
    <group ref={ref}>
      <Sphere />
      <Graticule />
    </group>
  );
}

export function Globe(props: DotsProps) {
  return (
    <Canvas
      camera={{ position: [0, 0, 5.5], fov: 38 }}
      dpr={[1, 2]}
      gl={{ antialias: true }}
    >
      <color attach="background" args={["#050810"]} />
      <ambientLight intensity={0.25} color="#9ca8c0" />
      <directionalLight
        position={[5, 3, 5]}
        intensity={1.4}
        color="#fff0d8"
      />
      <directionalLight
        position={[-6, -2, -4]}
        intensity={0.25}
        color="#5a7090"
      />
      <Stars />
      <Atmosphere />
      <AutoRotate enabled={props.personas.length === 0} />
      <Dots {...props} />
      <OrbitControls
        enablePan={false}
        enableZoom
        minDistance={3.2}
        maxDistance={10}
        rotateSpeed={0.4}
        zoomSpeed={0.5}
        autoRotate={false}
      />
    </Canvas>
  );
}
