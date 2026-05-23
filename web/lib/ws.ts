import type { AgentResponse, Forecast, Persona, SwarmSummary } from "./types";

const WS_BASE = process.env.NEXT_PUBLIC_WS_BASE || "ws://localhost:8000";

export interface StreamHandlers {
  onPersonas: (personas: Persona[]) => void;
  onResponse: (r: AgentResponse) => void;
  onDone: (
    forecast: Forecast | null,
    summary: SwarmSummary | null,
    error: string | null,
  ) => void;
}

export function openStream(runId: string, handlers: StreamHandlers): WebSocket {
  const ws = new WebSocket(`${WS_BASE}/swarm/run/${runId}/stream`);
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (Array.isArray(data.personas)) {
      handlers.onPersonas(data.personas);
    } else if (data.done) {
      handlers.onDone(
        data.forecast ?? null,
        data.summary ?? null,
        data.error ?? null,
      );
      ws.close();
    } else if (data.persona_id) {
      handlers.onResponse({
        persona_id: data.persona_id,
        position: data.position,
        confidence: data.confidence,
        reasoning: data.reasoning ?? "",
      });
    }
  };
  return ws;
}
