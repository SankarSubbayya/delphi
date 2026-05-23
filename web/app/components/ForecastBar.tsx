"use client";

import type { AgentResponse, Forecast, Mode } from "@/lib/types";

function formatHeadline(f: Forecast | null): string {
  if (!f || f.headline == null) return "—";
  if (typeof f.headline === "number") return `${(f.headline * 100).toFixed(1)}%`;
  return String(f.headline);
}

function formatCI(f: Forecast | null): string {
  if (!f?.confidence_interval) return "";
  const [lo, hi] = f.confidence_interval;
  return `[${(lo * 100).toFixed(0)}%, ${(hi * 100).toFixed(0)}%]`;
}

export function ForecastBar({
  forecast,
  mode,
  responses,
  totalPersonas,
  prevHeadline,
}: {
  forecast: Forecast | null;
  mode: Mode;
  responses: AgentResponse[];
  totalPersonas: number;
  prevHeadline: number | string | null;
}) {
  const progress = totalPersonas ? Math.min(1, responses.length / totalPersonas) : 0;

  const delta =
    forecast &&
    typeof forecast.headline === "number" &&
    typeof prevHeadline === "number"
      ? forecast.headline - prevHeadline
      : null;

  return (
    <div className="border-t border-ink-100 bg-parchment">
      <div className="px-8 py-5 flex items-end gap-10">
        <div>
          <div className="smcaps text-ink-300 mb-1">Headline</div>
          <div className="font-serif text-5xl text-ink-500 leading-none tabular-nums">
            {formatHeadline(forecast)}
          </div>
        </div>
        {forecast?.confidence_interval && (
          <div>
            <div className="smcaps text-ink-300 mb-1">±1σ band</div>
            <div className="text-ink-400 tabular-nums">{formatCI(forecast)}</div>
          </div>
        )}
        <div>
          <div className="smcaps text-ink-300 mb-1">n</div>
          <div className="text-ink-400 tabular-nums">
            {responses.length} / {totalPersonas || "—"}
            {forecast && forecast.n_failed > 0 && (
              <span className="text-burgundy ml-2">({forecast.n_failed} failed)</span>
            )}
          </div>
        </div>
        {delta !== null && (
          <div>
            <div className="smcaps text-ink-300 mb-1">Shift</div>
            <div
              className={`tabular-nums ${
                delta < 0 ? "text-burgundy" : "text-umber"
              }`}
            >
              {delta >= 0 ? "+" : ""}
              {(delta * 100).toFixed(1)} pp
            </div>
          </div>
        )}
        <div className="ml-auto smcaps text-ink-300">
          Mode · {mode.replace("_", " ")}
        </div>
      </div>

      <div className="px-8 pb-4">
        <div className="h-px bg-ink-50 mb-3">
          <div
            className="h-px bg-burgundy"
            style={{ width: `${progress * 100}%`, transition: "width 100ms linear" }}
          />
        </div>

        {forecast && (
          <div className="grid grid-cols-5 gap-3 mt-3">
            {Object.entries(forecast.distribution).map(([bucket, share]) => (
              <div key={bucket}>
                <div className="smcaps text-ink-300 mb-1">{bucket}</div>
                <div className="h-6 bg-cream relative">
                  <div
                    className="absolute inset-y-0 left-0 bg-ink-400"
                    style={{ width: `${share * 100}%` }}
                  />
                  <div className="absolute inset-0 flex items-center justify-end pr-2 text-[10px] text-ink-500 tabular-nums">
                    {(share * 100).toFixed(0)}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
