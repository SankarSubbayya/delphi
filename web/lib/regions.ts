// US Census Bureau divisions, with a representative-city centroid each.
export const REGION_COORDS: Record<string, [number, number]> = {
  "New England": [42.36, -71.06], // Boston
  "Mid-Atlantic": [40.71, -74.0], // New York
  "East North Central": [41.88, -87.63], // Chicago
  "West North Central": [44.98, -93.27], // Minneapolis
  "South Atlantic": [33.75, -84.39], // Atlanta
  "East South Central": [36.16, -86.78], // Nashville
  "West South Central": [29.76, -95.37], // Houston
  "Mountain": [39.74, -104.99], // Denver
  "Pacific": [37.77, -122.42], // San Francisco
};

const DEFAULT_COORDS: [number, number] = [39.83, -98.58];

export function regionCoords(region: string): [number, number] {
  return REGION_COORDS[region] ?? DEFAULT_COORDS;
}

export function deterministicJitter(seed: string, axis: number): number {
  let h = 0;
  for (let i = 0; i < seed.length; i++) {
    h = ((h * 31) ^ seed.charCodeAt(i)) | 0;
    h = (h ^ (axis * 2654435761)) | 0;
  }
  return (((h >>> 0) % 1000) / 1000) - 0.5;
}
