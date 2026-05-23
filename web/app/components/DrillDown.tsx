"use client";

import type { PersonaDetail } from "@/lib/types";

export function DrillDown({
  detail,
  loading,
  onClose,
}: {
  detail: PersonaDetail | null;
  loading: boolean;
  onClose: () => void;
}) {
  if (loading) {
    return (
      <div className="p-6 text-ink-300 smcaps">Loading…</div>
    );
  }

  if (!detail) {
    return (
      <div className="p-6 text-ink-300">
        <div className="smcaps mb-3">Drill-down</div>
        <p className="text-ink-200 italic">
          Select a dot on the globe to inspect one agent's persona and
          reasoning.
        </p>
      </div>
    );
  }

  const { persona, response } = detail;

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between border-b border-ink-100 px-6 py-3">
        <div className="smcaps text-ink-300">Persona dossier</div>
        <button
          onClick={onClose}
          className="smcaps text-ink-200 hover:text-burgundy"
          aria-label="Close"
        >
          Close
        </button>
      </div>

      <div className="px-6 py-4 border-b border-ink-100">
        <div className="font-serif text-xl text-ink-500 mb-2">
          {persona.label}
        </div>
        <p className="text-ink-400 italic leading-snug">
          {persona.identity_prompt}
        </p>
      </div>

      <div className="px-6 py-4 border-b border-ink-100 space-y-1">
        {Object.entries(persona.demographics).map(([k, v]) => (
          <div key={k} className="flex justify-between text-ink-400">
            <span className="smcaps text-ink-300">{k.replace("_", " ")}</span>
            <span>{String(v)}</span>
          </div>
        ))}
      </div>

      {response ? (
        <div className="px-6 py-4 overflow-y-auto flex-1">
          <div className="flex items-baseline gap-4 mb-3">
            <div>
              <div className="smcaps text-ink-300 mb-1">Position</div>
              <div className="font-serif text-2xl text-ink-500 tabular-nums">
                {typeof response.position === "number"
                  ? `${(response.position * 100).toFixed(0)}%`
                  : String(response.position ?? "—")}
              </div>
            </div>
            <div>
              <div className="smcaps text-ink-300 mb-1">Confidence</div>
              <div className="text-ink-400 tabular-nums">
                {(response.confidence * 100).toFixed(0)}%
              </div>
            </div>
          </div>

          <div className="smcaps text-ink-300 mb-1">Reasoning</div>
          <p className="text-ink-500 leading-relaxed mb-4">
            {response.reasoning}
          </p>

          {response.sources && response.sources.length > 0 && (
            <>
              <div className="smcaps text-ink-300 mb-1">Sources</div>
              <ul className="space-y-1">
                {response.sources.map((s, i) => (
                  <li key={i}>
                    <a
                      href={s.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-burgundy hover:underline break-all"
                    >
                      {s.title || s.url}
                    </a>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      ) : (
        <div className="px-6 py-4 text-ink-300 italic">
          This agent has not yet finished reasoning.
        </div>
      )}
    </div>
  );
}
