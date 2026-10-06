"use client";

import { useEffect, useState } from "react";

import type { Source } from "@/lib/api";
import { LevelBadge } from "./LevelBadge";

export function SourceList({ sources, messageId }: { sources: Source[]; messageId: string }) {
  const [open, setOpen] = useState(false);

  // A citation chip links to "#src-<message>-<n>": open the list so the card exists to scroll to.
  useEffect(() => {
    const openIfTargeted = () => {
      if (window.location.hash.startsWith(`#src-${messageId}-`)) {
        setOpen(true);
        requestAnimationFrame(() => document.querySelector(window.location.hash)?.scrollIntoView({ block: "center" }));
      }
    };
    window.addEventListener("hashchange", openIfTargeted);
    return () => window.removeEventListener("hashchange", openIfTargeted);
  }, [messageId]);

  if (sources.length === 0) return null;

  return (
    <div className="mt-3">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 text-xs text-neutral-400 hover:text-neutral-200"
      >
        <span className={`transition-transform ${open ? "rotate-90" : ""}`}>›</span>
        {sources.length} source{sources.length > 1 ? "s" : ""} consultée{sources.length > 1 ? "s" : ""}
      </button>
      {open && (
        <ol className="mt-2 space-y-2">
          {sources.map((source, i) => (
            <SourceCard key={source.reference} source={source} anchor={sourceAnchor(messageId, i)} />
          ))}
        </ol>
      )}
    </div>
  );
}

function SourceCard({ source, anchor }: { source: Source; anchor: string }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <li id={anchor} className="scroll-mt-24 rounded-lg border border-neutral-800 bg-neutral-900/60 p-3 target:border-sky-500/60">
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-sm font-medium text-neutral-100">{source.reference}</span>
        <LevelBadge level={source.access_level} />
        <span className="text-[11px] text-neutral-500">{source.portee}</span>
        <span className="ml-auto font-mono text-[11px] text-neutral-500">{source.score.toFixed(3)}</span>
      </div>
      {source.heading && <p className="mt-1 text-xs text-neutral-400">{source.heading}</p>}
      <p className={`mt-2 whitespace-pre-line text-xs leading-relaxed text-neutral-300 ${expanded ? "" : "line-clamp-3"}`}>
        {source.text}
      </p>
      <button
        type="button"
        onClick={() => setExpanded(!expanded)}
        className="mt-1 text-[11px] text-sky-400 hover:text-sky-300"
      >
        {expanded ? "Réduire" : "Afficher l’extrait"}
      </button>
    </li>
  );
}

export function sourceAnchor(messageId: string, index: number): string {
  return `src-${messageId}-${index}`;
}
