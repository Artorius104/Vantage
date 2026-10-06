"use client";

import type { RoleInfo } from "@/lib/api";
import type { Conversation } from "@/lib/conversations";
import { LevelBadge } from "./LevelBadge";

type Props = {
  roles: RoleInfo[];
  role: string;
  conversations: Conversation[];
  activeId: string | null;
  onRoleChange: (role: string) => void;
  onSelect: (id: string) => void;
  onNew: () => void;
  onDelete: (id: string) => void;
};

export function Sidebar({ roles, role, conversations, activeId, onRoleChange, onSelect, onNew, onDelete }: Props) {
  const current = roles.find((r) => r.id === role);
  const sorted = [...conversations].sort((a, b) => b.updatedAt - a.updatedAt);

  return (
    <aside className="flex h-full w-64 shrink-0 flex-col bg-neutral-950 px-3 py-4">
      <div className="flex items-center gap-2 px-2">
        <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-sky-600 text-sm font-bold text-white">V</div>
        <span className="text-[15px] font-semibold text-neutral-100">Vantage</span>
      </div>

      <button
        type="button"
        onClick={onNew}
        className="mt-5 flex items-center gap-2 rounded-lg px-2 py-2 text-sm text-neutral-200 hover:bg-neutral-800/70"
      >
        <svg viewBox="0 0 16 16" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true">
          <path d="M8 3v10M3 8h10" strokeLinecap="round" />
        </svg>
        Nouvelle conversation
      </button>

      <p className="mt-5 px-2 text-[11px] font-medium uppercase tracking-wide text-neutral-500">Conversations · {role}</p>
      <nav className="mt-1 flex-1 space-y-0.5 overflow-y-auto">
        {sorted.length === 0 && <p className="px-2 py-2 text-xs text-neutral-600">Aucune conversation</p>}
        {sorted.map((conversation) => (
          <div
            key={conversation.id}
            className={`group flex items-center rounded-lg ${
              conversation.id === activeId ? "bg-neutral-800" : "hover:bg-neutral-800/60"
            }`}
          >
            <button
              type="button"
              onClick={() => onSelect(conversation.id)}
              className="min-w-0 flex-1 truncate px-2 py-2 text-left text-sm text-neutral-300"
            >
              {conversation.title}
            </button>
            <button
              type="button"
              onClick={() => onDelete(conversation.id)}
              aria-label="Supprimer la conversation"
              className="mr-1 hidden rounded px-1.5 text-neutral-500 hover:text-rose-400 group-hover:block"
            >
              ×
            </button>
          </div>
        ))}
      </nav>

      <div className="mt-3 border-t border-neutral-800 pt-3">
        <label htmlFor="role" className="px-2 text-[11px] font-medium uppercase tracking-wide text-neutral-500">
          Rôle
        </label>
        <select
          id="role"
          value={role}
          onChange={(e) => onRoleChange(e.target.value)}
          className="mt-1 w-full rounded-lg border border-neutral-800 bg-neutral-900 px-2 py-2 text-sm text-neutral-100 focus:border-neutral-600 focus:outline-none"
        >
          {roles.map((r) => (
            <option key={r.id} value={r.id}>
              {r.id}
            </option>
          ))}
        </select>
        {current && (
          <div className="mt-2 flex flex-wrap gap-1 px-1">
            {current.levels.map((level) => (
              <LevelBadge key={level} level={level} />
            ))}
          </div>
        )}
      </div>
    </aside>
  );
}
