interface ProgressBarProps {
  percent: number;
  label?: string;
  showValue?: boolean;
}

export default function ProgressBar({ percent, label, showValue = true }: ProgressBarProps) {
  const clamped = Math.max(0, Math.min(100, percent));
  return (
    <div>
      {label && (
        <div className="mb-2 flex items-baseline justify-between">
          <span className="text-[15px] font-medium text-ink-700">{label}</span>
          {showValue && <span className="font-mono text-[15px] text-ink">{clamped}%</span>}
        </div>
      )}
      <div className="h-2.5 w-full overflow-hidden rounded-full bg-ink-700/10 shadow-inner">
        <div
          className="h-full rounded-full bg-growth transition-all duration-500"
          style={{ width: `${clamped}%` }}
        />
      </div>
    </div>
  );
}
