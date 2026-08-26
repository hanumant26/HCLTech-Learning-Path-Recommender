import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAsyncData } from "../hooks/useAsyncData";
import { getRecommendations } from "../services/api";
import { ResourceType } from "../types";
import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import EmptyState from "../components/common/EmptyState";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";

type FilterTab = "all" | ResourceType;

const tabs: { id: FilterTab; label: string }[] = [
  { id: "all", label: "All" },
  { id: "course", label: "Courses" },
  { id: "project", label: "Projects" },
  { id: "practice", label: "Practice" },
  { id: "assessment", label: "Assessments" },
];

export default function Recommendations() {
  const navigate = useNavigate();
  const { data: recs, loading, error, reload } = useAsyncData(getRecommendations);
  const [tab, setTab] = useState<FilterTab>("all");

  if (loading) return <LoadingState label="Scoring recommendations" />;
  if (error) return <ErrorState message={error} onRetry={reload} />;

  const filtered = (recs ?? []).filter((r) => tab === "all" || r.type === tab);

  return (
    <div className="container-page page-shell">
      <h1 className="text-page-title">Recommended for you</h1>
      <p className="text-page-subtitle">Ranked by fit against your skill gaps and goal.</p>

      <div className="mt-6 flex flex-wrap gap-2">
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`rounded-full px-4 py-1.5 text-sm font-medium transition ${
              tab === t.id ? "bg-ink text-paper" : "bg-ink-700/10 text-ink-700 hover:bg-ink-700/20"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {filtered.length === 0 ? (
        <div className="mt-8">
          <EmptyState
            title="Nothing here yet"
            description="Try a different filter, or check back after your skill assessment updates."
          />
        </div>
      ) : (
        <div className="mt-8 grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
          {filtered.map((r) => (
            <Card key={r.id} onClick={() => navigate(`/resource/${r.id}`)}>
              <div className="mb-2 flex flex-wrap items-center gap-2">
                <Badge>{r.type}</Badge>
                <Badge>{r.difficulty}</Badge>
                <span className="ml-auto font-mono text-xs text-growth-dark">{r.score}% match</span>
              </div>
              <p className="text-card-title">{r.title}</p>
              <p className="mt-1.5 text-sm text-ink-700">{r.reason}</p>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {r.skillsCovered.map((s) => (
                  <span key={s} className="rounded-full bg-ink-700/10 px-2 py-0.5 text-[11px] text-ink-700">
                    {s}
                  </span>
                ))}
              </div>
              <p className="mt-3 font-mono text-xs text-ink-700/70">{r.estimatedHours} hrs estimated</p>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
