interface ErrorStateProps {
  message: string;
  onRetry?: () => void;
}

export default function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center gap-3 rounded-xl2 border border-clay/30 bg-clay-light px-6 py-10 text-center">
      <p className="font-display text-lg text-clay">Couldn't load this.</p>
      <p className="max-w-sm text-sm text-ink-700">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-2 btn-primary"
        >
          Try again
        </button>
      )}
    </div>
  );
}
