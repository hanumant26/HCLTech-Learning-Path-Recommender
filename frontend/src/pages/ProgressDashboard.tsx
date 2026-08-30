import { Link, useNavigate } from "react-router-dom";
import { useAsyncData } from "../hooks/useAsyncData";
import { getProgress } from "../services/api";
import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import ProgressBar from "../components/common/ProgressBar";
import Card from "../components/common/Card";

export default function ProgressDashboard() {
  const navigate = useNavigate();
  const { data: progress, loading, error, reload } = useAsyncData(getProgress);

  if (loading) return <LoadingState label="Loading your progress" />;
  if (error) return <ErrorState message={error} onRetry={reload} />;
  if (!progress) return null;

  const stats = [
    { label: "Skills developed", value: progress.skillsDeveloped },
    { label: "Courses completed", value: progress.coursesCompleted },
    { label: "Projects completed", value: progress.projectsCompleted },
  ];

  return (
    <div className="container-medium page-shell">
      <h1 className="text-page-title">Your progress</h1>
      <p className="text-page-subtitle">Current phase: {progress.currentPhase}</p>

      <div className="mt-6 rounded-xl2 border border-ink-700/10 bg-surface p-6">
        <ProgressBar percent={progress.overallPercent} label="Overall completion" />
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-3">
        {stats.map((s) => (
          <Card key={s.label}>
            <p className="font-display text-3xl text-ink">{s.value}</p>
            <p className="mt-1 text-sm text-ink-700">{s.label}</p>
          </Card>
        ))}
      </div>

      <div className="mt-8 flex flex-wrap items-center justify-between gap-2">
        <p className="text-section-heading">Milestones</p>
        <div className="flex gap-4">
          <Link to="/achievements" className="text-sm text-ink-700 underline decoration-dotted hover:text-ink">
            View achievements →
          </Link>
          <Link to="/activity" className="text-sm text-ink-700 underline decoration-dotted hover:text-ink">
            View full activity →
          </Link>
        </div>
      </div>
      <ul className="mt-3 space-y-2">
          {progress.milestones.map((m) => (
            <li
              key={m.title}
              className="flex items-center gap-3 rounded-xl2 border border-ink-700/10 bg-surface px-4 py-3"
            >
              <span
                className={`flex h-5 w-5 flex-none items-center justify-center rounded-full text-[11px] text-white ${
                  m.done ? "bg-growth" : "bg-ink-700/20"
                }`}
              >
                {m.done ? "✓" : ""}
              </span>
              <span className={`text-sm ${m.done ? "text-ink-700 line-through" : "text-ink"}`}>
                {m.title}
              </span>
            </li>
          ))}
        </ul>

      <div className="mt-8 rounded-xl2 border border-amber/30 bg-amber-light p-5">
        <p className="font-mono text-xs uppercase tracking-wide text-amber">Next action</p>
        <p className="mt-1 text-ink">{progress.nextAction}</p>
        <button
          onClick={() => navigate("/roadmap")}
          className="mt-3 btn-primary"
        >
          Go to roadmap
        </button>
      </div>
    </div>
  );
}
