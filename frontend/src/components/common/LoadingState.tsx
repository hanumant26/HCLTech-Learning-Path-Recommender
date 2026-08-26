interface LoadingStateProps {
  label?: string;
}

export default function LoadingState({ label = "Loading" }: LoadingStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-16 text-ink-600">
      <div className="h-8 w-8 animate-spin rounded-full border-2 border-ink-600/30 border-t-growth" />
      <p className="font-mono text-sm tracking-wide">{label}…</p>
    </div>
  );
}
