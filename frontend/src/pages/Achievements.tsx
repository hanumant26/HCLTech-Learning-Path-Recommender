import { useAsyncData } from "../hooks/useAsyncData";
import { getAchievements, getStreak } from "../services/api";
import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";

const dayLabels = ["M", "T", "W", "T", "F", "S", "S"];

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

export default function Achievements() {
  const { data: achievements, loading: loadingA, error: errorA, reload: reloadA } = useAsyncData(getAchievements);
  const { data: streak, loading: loadingS, error: errorS, reload: reloadS } = useAsyncData(getStreak);

  const loading = loadingA || loadingS;
  const error = errorA || errorS;

  if (loading) return <LoadingState label="Loading your achievements" />;
  if (error) return <ErrorState message={error} onRetry={() => { reloadA(); reloadS(); }} />;
  if (!achievements || !streak) return null;

  const earnedCount = achievements.filter((a) => a.earned).length;

  return (
    <div className="container-medium page-shell">
      <h1 className="text-page-title">Achievements</h1>
      <p className="text-page-subtitle">
        {earnedCount} of {achievements.length} earned
      </p>

      {/* --- Streak --- */}
      <div className="mt-8 rounded-xl2 border border-amber/30 bg-amber-light p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="font-mono text-xs uppercase tracking-wide text-amber">Current streak</p>
            <p className="mt-1 font-display text-4xl font-semibold text-ink">
              🔥 {streak.currentStreak} {streak.currentStreak === 1 ? "day" : "days"}
            </p>
          </div>
          <div className="text-right">
            <p className="font-mono text-xs uppercase tracking-wide text-amber">Longest</p>
            <p className="mt-1 font-display text-2xl text-ink">{streak.longestStreak} days</p>
          </div>
        </div>

        <div className="mt-5 flex justify-between gap-1.5">
          {streak.activeDaysThisWeek.map((active, i) => (
            <div key={i} className="flex flex-1 flex-col items-center gap-1.5">
              <div
                className={`flex h-9 w-9 items-center justify-center rounded-full text-xs ${
                  active ? "bg-amber text-white" : "border border-ink-700/20 text-ink-700/50"
                }`}
              >
                {active ? "✓" : ""}
              </div>
              <span className="font-mono text-[10px] text-ink-700">{dayLabels[i]}</span>
            </div>
          ))}
        </div>

        <p className="mt-4 text-xs text-ink-700">
          Last active {formatDate(streak.lastActiveDate)}. Complete something today to keep your
          streak going.
        </p>
      </div>

      {/* --- Achievement badges --- */}
      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {achievements.map((a) => (
          <div
            key={a.id}
            className={`flex gap-3 rounded-xl2 border p-4 transition ${
              a.earned
                ? "border-growth/30 bg-growth-light"
                : "border-ink-700/10 bg-surface opacity-60"
            }`}
          >
            <span className={`text-2xl ${a.earned ? "" : "grayscale"}`} aria-hidden="true">
              {a.icon}
            </span>
            <div className="min-w-0 flex-1">
              <p className="font-display text-base text-ink">{a.title}</p>
              <p className="mt-0.5 text-sm text-ink-700">{a.description}</p>
              {a.earned && a.earnedAt && (
                <p className="mt-1 font-mono text-[11px] text-growth-dark">
                  Earned {formatDate(a.earnedAt)}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
