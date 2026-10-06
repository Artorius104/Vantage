import type { AccessLevel } from "@/lib/api";

const STYLES: Record<AccessLevel, string> = {
  public: "bg-emerald-500/15 text-emerald-300 ring-emerald-500/30",
  interne: "bg-amber-500/15 text-amber-300 ring-amber-500/30",
  confidentiel: "bg-rose-500/15 text-rose-300 ring-rose-500/30",
};

export function LevelBadge({ level }: { level: AccessLevel }) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-[11px] font-medium ring-1 ring-inset ${STYLES[level]}`}>
      {level}
    </span>
  );
}
