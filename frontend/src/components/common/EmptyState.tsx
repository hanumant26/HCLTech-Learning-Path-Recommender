interface EmptyStateProps {
  title: string;
  description?: string;
  action?: { label: string; onClick: () => void };
}

export default function EmptyState({ title, description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center gap-2 rounded-xl2 border border-dashed border-ink-600/30 bg-paper-dim px-6 py-14 text-center">
      <p className="font-display text-lg text-ink">{title}</p>
      {description && <p className="max-w-sm text-sm text-ink-700">{description}</p>}
      {action && (
        <button
          onClick={action.onClick}
          className="mt-3 rounded-full border border-ink px-5 py-2 text-sm font-medium text-ink transition hover:bg-ink hover:text-paper"
        >
          {action.label}
        </button>
      )}
    </div>
  );
}
