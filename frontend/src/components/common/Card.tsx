interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export default function Card({ children, className = "", onClick }: CardProps) {
  const interactive = Boolean(onClick);
  return (
    <div
      onClick={onClick}
      className={`rounded-xl2 border border-ink-700/10 bg-surface p-6 shadow-sm backdrop-blur-sm transition ${
        interactive ? "cursor-pointer hover:-translate-y-0.5 hover:border-ink-700/20 hover:shadow-md" : ""
      } ${className}`}
    >
      {children}
    </div>
  );
}
