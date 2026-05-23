export type Mode = "forecast" | "pretest" | "stress_test" | "open";

export interface Persona {
  id: string;
  label: string;
  demographics: {
    age: string;
    region: string;
    education: string;
    occupation: string;
    belief_axis: string;
  };
  identity_prompt: string;
}

export interface Source {
  url: string;
  title: string;
  snippet: string;
}

export interface AgentResponse {
  persona_id: string;
  position: number | string | null;
  confidence: number;
  reasoning: string;
  sources?: Source[];
}

export interface Forecast {
  question: string;
  mode: Mode;
  n_personas: number;
  n_failed: number;
  headline: number | string | null;
  confidence_interval: [number, number] | null;
  distribution: Record<string, number>;
  by_demographic: Record<string, Record<string, { n: number; mean?: number | null; top?: string | null }>>;
}

export interface PersonaDetail {
  persona: Persona;
  response: AgentResponse | null;
}

export interface SwarmSummary {
  headline_narrative: string;
  top_reasons_for: string[];
  top_reasons_against: string[];
  demographic_split: string;
  outlier_quote: string;
  outlier_attribution: string;
}
