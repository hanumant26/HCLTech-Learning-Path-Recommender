interface BadgeProps {
  children: React.ReactNode;
  tone?: "neutral" | "growth" | "amber" | "clay";
}

const toneClasses: Record<string, string> = {
  neutral: "bg-ink-700/10 text-ink-700",
  growth: "bg-growth-light text-growth-dark",
  amber: "bg-amber-light text-amber",
  clay: "bg-clay-light text-clay",
};

export default function Badge({ children, tone = "neutral" }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-1 font-mono text-[12px] uppercase tracking-wide ${toneClasses[tone]}`}
    >
      {children}
    </span>
  );
}
