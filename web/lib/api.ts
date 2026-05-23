import type { Forecast, Mode, PersonaDetail, SwarmSummary } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export async function createRun(req: {
  question: string;
  n_personas: number;
  mode: Mode;
}): Promise<{ run_id: string; status_url: string }> {
  const r = await fetch(`${API_BASE}/swarm/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!r.ok) throw new Error(`createRun ${r.status}`);
  return r.json();
}

export async function getPersona(runId: string, personaId: string): Promise<PersonaDetail> {
  const r = await fetch(`${API_BASE}/swarm/run/${runId}/persona/${personaId}`);
  if (!r.ok) throw new Error(`getPersona ${r.status}`);
  return r.json();
}

export async function postShock(
  runId: string,
  shock: string,
): Promise<{ forecast: Forecast; summary: SwarmSummary | null }> {
  const r = await fetch(`${API_BASE}/swarm/run/${runId}/shock`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ shock }),
  });
  if (!r.ok) throw new Error(`postShock ${r.status}`);
  return r.json();
}
