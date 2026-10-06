"use client";

import { useState } from "react";

type Props = {
  disabled: boolean;
  busy: boolean;
  onSend: (question: string) => void;
  onStop: () => void;
};

export function Composer({ disabled, busy, onSend, onStop }: Props) {
  const [value, setValue] = useState("");

  const send = () => {
    const question = value.trim();
    if (!question || busy || disabled) return;
    onSend(question);
    setValue("");
  };

  return (
    <div className="rounded-3xl border border-neutral-800 bg-neutral-900 px-4 py-3 shadow-lg focus-within:border-neutral-700">
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
            e.preventDefault();
            send();
          }
        }}
        rows={1}
        placeholder="Posez une question à Vantage…"
        disabled={disabled}
        className="field-sizing-content max-h-48 w-full resize-none bg-transparent text-[15px] text-neutral-100 placeholder:text-neutral-500 focus:outline-none"
      />
      <div className="mt-2 flex items-center justify-between">
        <span className="text-[11px] text-neutral-500">Entrée pour envoyer · Maj+Entrée pour un saut de ligne</span>
        {busy ? (
          <button
            type="button"
            onClick={onStop}
            className="rounded-full bg-neutral-200 px-3 py-1 text-xs font-medium text-neutral-900 hover:bg-white"
          >
            Arrêter
          </button>
        ) : (
          <button
            type="button"
            onClick={send}
            disabled={!value.trim() || disabled}
            aria-label="Envoyer"
            className="flex h-8 w-8 items-center justify-center rounded-full bg-neutral-100 text-neutral-900 hover:bg-white disabled:bg-neutral-700 disabled:text-neutral-500"
          >
            ↑
          </button>
        )}
      </div>
    </div>
  );
}
