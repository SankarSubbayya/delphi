"use client";

import type { SwarmSummary } from "@/lib/types";

export function SwarmSummaryPanel({
  summary,
  pending,
}: {
  summary: SwarmSummary | null;
  pending: boolean;
}) {
  if (pending) {
    return (
      <div className="border-t border-ink-100 px-8 py-5 bg-cream/40">
        <div className="smcaps text-ink-300">Synthesizing population narrative…</div>
      </div>
    );
  }

  if (!summary) return null;

  return (
    <div
      className="border-t border-ink-100 bg-cream/60 overflow-y-auto"
      style={{ maxHeight: "38vh" }}
    >
      <div className="px-8 pt-5 pb-3">
        <div className="smcaps text-ink-300 mb-2">Population synthesis</div>
        <p className="font-serif text-xl text-ink-500 leading-snug max-w-5xl">
          {summary.headline_narrative}
        </p>
      </div>

      <div className="px-8 pb-5 grid grid-cols-2 gap-10 max-w-6xl">
        <div>
          <div className="smcaps text-ink-300 mb-2">Strongest reasons for</div>
          <ul className="space-y-1.5 text-ink-500 leading-snug">
            {summary.top_reasons_for.map((r, i) => (
              <li key={i} className="flex">
                <span className="text-burgundy mr-2 select-none">·</span>
                <span>{r}</span>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <div className="smcaps text-ink-300 mb-2">Strongest reasons against</div>
          <ul className="space-y-1.5 text-ink-500 leading-snug">
            {summary.top_reasons_against.map((r, i) => (
              <li key={i} className="flex">
                <span className="text-burgundy mr-2 select-none">·</span>
                <span>{r}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="px-8 pb-4 border-t border-ink-100 pt-3">
        <div className="smcaps text-ink-300 mb-1">Demographic split</div>
        <p className="text-ink-500 leading-snug max-w-5xl">{summary.demographic_split}</p>
      </div>

      <div className="px-8 pb-6 border-t border-ink-100 pt-4">
        <blockquote className="font-serif italic text-2xl text-ink-500 leading-snug max-w-5xl">
          &ldquo;{summary.outlier_quote}&rdquo;
        </blockquote>
        <div className="smcaps text-ink-300 mt-2">— {summary.outlier_attribution}</div>
      </div>
    </div>
  );
}
