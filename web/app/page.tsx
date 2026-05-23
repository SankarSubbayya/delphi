"use client";

import dynamic from "next/dynamic";
import { useEffect, useRef, useState } from "react";
import { DrillDown } from "./components/DrillDown";
import { ForecastBar } from "./components/ForecastBar";
import { ModeToggle } from "./components/ModeToggle";
import { ShockInput } from "./components/ShockInput";
import { SwarmSummaryPanel } from "./components/SwarmSummary";
import { createRun, getPersona, postShock } from "@/lib/api";
import { openStream } from "@/lib/ws";
import type {
  AgentResponse,
  Forecast,
  Mode,
  Persona,
  PersonaDetail,
  SwarmSummary,
} from "@/lib/types";

const Globe = dynamic(() => import("./components/Globe").then((m) => m.Globe), {
  ssr: false,
  loading: () => (
    <div className="h-full flex items-center justify-center text-ink-200 smcaps">
      loading globe…
    </div>
  ),
});

type Status = "idle" | "running" | "done" | "error";

export default function Page() {
  const [question, setQuestion] = useState(
    "Will Apple ship smart glasses in 2027?",
  );
  const [n, setN] = useState(20);
  const [mode, setMode] = useState<Mode>("forecast");

  const [runId, setRunId] = useState<string | null>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [responses, setResponses] = useState<Record<string, AgentResponse>>({});
  const [forecast, setForecast] = useState<Forecast | null>(null);
  const [summary, setSummary] = useState<SwarmSummary | null>(null);
  const [prevHeadline, setPrevHeadline] = useState<number | string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [selectedDetail, setSelectedDetail] = useState<PersonaDetail | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    return () => {
      wsRef.current?.close();
    };
  }, []);

  async function handleRun() {
    setStatus("running");
    setError(null);
    setPersonas([]);
    setResponses({});
    setPrevHeadline(forecast?.headline ?? null);
    setForecast(null);
    setSummary(null);
    setSelectedId(null);
    setSelectedDetail(null);

    try {
      const { run_id } = await createRun({ question, n_personas: n, mode });
      setRunId(run_id);
      wsRef.current?.close();
      wsRef.current = openStream(run_id, {
        onPersonas: (ps) => setPersonas(ps),
        onResponse: (r) =>
          setResponses((prev) => ({ ...prev, [r.persona_id]: r })),
        onDone: (f, s, err) => {
          setForecast(f);
          setSummary(s);
          setError(err);
          setStatus(err ? "error" : "done");
        },
      });
    } catch (e) {
      setError(String(e));
      setStatus("error");
    }
  }

  async function handleSelect(id: string) {
    if (!runId) return;
    setSelectedId(id);
    setLoadingDetail(true);
    try {
      const detail = await getPersona(runId, id);
      setSelectedDetail(detail);
    } catch {
      setSelectedDetail(null);
    } finally {
      setLoadingDetail(false);
    }
  }

  async function handleShock(shock: string) {
    if (!runId) return;
    setPrevHeadline(forecast?.headline ?? null);
    setSummary(null);
    setStatus("running");
    try {
      const { forecast: f, summary: s } = await postShock(runId, shock);
      setForecast(f);
      setSummary(s);
      setStatus("done");
    } catch (e) {
      setError(String(e));
      setStatus("error");
    }
  }

  const responsesList = Object.values(responses);

  return (
    <main className="h-screen flex flex-col bg-parchment text-ink-500">
      <header className="border-b border-ink-100 px-8 py-4 flex items-baseline gap-6">
        <h1 className="font-serif text-3xl text-ink-500 leading-none">
          Delphi
        </h1>
        <div className="smcaps text-ink-300">
          Synthetic populations · reasoning at scale
        </div>
        <div className="ml-auto smcaps text-ink-300 tabular-nums">
          {status === "running" && "running"}
          {status === "done" && "ready"}
          {status === "error" && <span className="text-burgundy">error</span>}
        </div>
      </header>

      <div className="flex flex-1 min-h-0">
        <aside className="w-80 border-r border-ink-100 px-6 py-5 flex flex-col">
          <label className="block">
            <div className="smcaps text-ink-300 mb-2">Question</div>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              rows={4}
              className="w-full bg-cream border border-ink-100 px-3 py-2 text-ink-500 focus:border-burgundy focus:outline-none resize-none leading-snug"
            />
          </label>

          <div className="mt-5">
            <div className="smcaps text-ink-300 mb-2">Mode</div>
            <ModeToggle mode={mode} onChange={setMode} />
          </div>

          <label className="mt-5 block">
            <div className="smcaps text-ink-300 mb-2">
              N personas
              <span className="ml-1 text-ink-200">[5–500]</span>
            </div>
            <input
              type="number"
              value={n}
              min={5}
              max={500}
              onChange={(e) =>
                setN(Math.max(5, Math.min(500, Number(e.target.value) || 0)))
              }
              className="w-full bg-cream border border-ink-100 px-3 py-2 text-ink-500 focus:border-burgundy focus:outline-none tabular-nums"
            />
          </label>

          <button
            onClick={handleRun}
            disabled={status === "running" || !question.trim()}
            className="mt-5 w-full bg-burgundy text-parchment smcaps py-3 hover:bg-burgundy-dark disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {status === "running" ? "Running…" : "Convene swarm"}
          </button>

          {error && (
            <div className="mt-3 text-burgundy text-xs break-words">
              {error}
            </div>
          )}

          <ShockInput
            onSubmit={handleShock}
            disabled={status === "running" || !runId || !forecast}
          />
        </aside>

        <section className="flex-1 flex flex-col min-w-0">
          <div className="flex-1 min-h-0 bg-ink-900 relative">
            {personas.length > 0 ? (
              <Globe
                personas={personas}
                responses={responses}
                mode={mode}
                onSelect={handleSelect}
                selectedId={selectedId}
              />
            ) : (
              <div className="h-full flex items-center justify-center text-ink-100 smcaps">
                {status === "running"
                  ? "Sampling demographic vectors…"
                  : "Convene a swarm to populate the globe"}
              </div>
            )}
            <div className="absolute top-4 left-4 text-ink-50 smcaps tabular-nums pointer-events-none">
              {personas.length > 0 &&
                `${responsesList.filter((r) => r.position != null).length} / ${personas.length}`}
            </div>
          </div>

          <ForecastBar
            forecast={forecast}
            mode={mode}
            responses={responsesList}
            totalPersonas={personas.length}
            prevHeadline={prevHeadline}
          />

          <SwarmSummaryPanel
            summary={summary}
            pending={status === "running" && responsesList.length >= personas.length && personas.length > 0}
          />
        </section>

        <aside className="w-96 border-l border-ink-100 flex flex-col min-h-0">
          <DrillDown
            detail={selectedId ? selectedDetail : null}
            loading={loadingDetail}
            onClose={() => {
              setSelectedId(null);
              setSelectedDetail(null);
            }}
          />
        </aside>
      </div>
    </main>
  );
}
