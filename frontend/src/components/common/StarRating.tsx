interface StarRatingProps {
  rating: number; // 0-5
}

export default function StarRating({ rating }: StarRatingProps) {
  const rounded = Math.round(rating * 2) / 2;
  return (
    <span className="inline-flex items-center gap-1 font-mono text-xs text-ink-700">
      <span className="text-amber" aria-hidden="true">
        {"★".repeat(Math.floor(rounded))}
        {rounded % 1 !== 0 ? "½" : ""}
      </span>
      {rating.toFixed(1)}
    </span>
  );
}
