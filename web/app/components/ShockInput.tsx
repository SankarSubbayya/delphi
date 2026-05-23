"use client";

import { useState } from "react";

export function ShockInput({
  onSubmit,
  disabled,
}: {
  onSubmit: (shock: string) => void;
  disabled?: boolean;
}) {
  const [text, setText] = useState("");

  const submit = () => {
    const t = text.trim();
    if (!t) return;
    onSubmit(t);
    setText("");
  };

  return (
    <div className="border-t border-ink-100 pt-4 mt-auto">
      <div className="smcaps text-ink-300 mb-2">News shock</div>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        disabled={disabled}
        placeholder="A new event arrives. Re-run with this in context."
        rows={3}
        className="w-full bg-cream border border-ink-100 px-3 py-2 text-ink-500 placeholder-ink-200 focus:border-burgundy focus:outline-none resize-none"
      />
      <button
        onClick={submit}
        disabled={disabled || !text.trim()}
        className="mt-2 w-full bg-burgundy text-parchment smcaps py-2 hover:bg-burgundy-dark disabled:opacity-40 disabled:cursor-not-allowed"
      >
        Inject shock
      </button>
    </div>
  );
}
