"use client";

import type { Mode } from "@/lib/types";

const MODES: { value: Mode; label: string }[] = [
  { value: "forecast", label: "Forecast" },
  { value: "pretest", label: "Pretest" },
  { value: "stress_test", label: "Stress" },
];

export function ModeToggle({
  mode,
  onChange,
}: {
  mode: Mode;
  onChange: (m: Mode) => void;
}) {
  return (
    <div className="flex border border-ink-100">
      {MODES.map((m, i) => (
        <button
          key={m.value}
          type="button"
          onClick={() => onChange(m.value)}
          className={[
            "px-3 py-1.5 smcaps flex-1 transition-colors",
            i < MODES.length - 1 ? "border-r border-ink-100" : "",
            mode === m.value
              ? "bg-ink-500 text-parchment"
              : "bg-parchment hover:bg-cream text-ink-400",
          ].join(" ")}
        >
          {m.label}
        </button>
      ))}
    </div>
  );
}
