import { useNavigate } from "react-router-dom";
import { useAsyncData } from "../hooks/useAsyncData";
import { getRecommendations, getProfile } from "../services/api";
import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import Badge from "../components/common/Badge";

const tourSteps = [
  {
    title: "Skill assessment",
    body: "Rate what you already know so we can see the real gaps, not guessed ones.",
  },
  {
    title: "Recommendations",
    body: "Courses, projects, and practice — ranked by how much they close your gaps.",
  },
  {
    title: "Roadmap",
    body: "Everything in prerequisite order, with locked steps that unlock as you go.",
  },
];

export default function Welcome() {
  const navigate = useNavigate();
  const { data: profile } = useAsyncData(getProfile);
  const { data: recs, loading, error, reload } = useAsyncData(getRecommendations);

  if (loading) return <LoadingState label="Setting things up" />;
  if (error) return <ErrorState message={error} onRetry={reload} />;

  const topPick = recs ? [...recs].sort((a, b) => b.score - a.score)[0] : undefined;

  return (
    <div className="container-form page-shell text-center">
      <p className="font-mono text-xs uppercase tracking-[0.2em] text-growth-dark">
        Profile complete
      </p>
      <h1 className="mt-3 text-page-title">
        You're set{profile?.name ? `, ${profile.name.split(" ")[0]}` : ""}.
      </h1>
      <p className="text-page-subtitle">
        Here's what we'd start with, and a quick look at how the rest of this works.
      </p>

      {topPick && (
        <div className="mt-8 rounded-xl2 border border-growth/30 bg-growth-light p-6 text-left">
          <p className="font-mono text-xs uppercase tracking-wide text-growth-dark">
            Your first recommendation
          </p>
          <div className="mt-2 flex flex-wrap items-center gap-2">
            <Badge>{topPick.type}</Badge>
            <Badge>{topPick.difficulty}</Badge>
            <span className="font-mono text-xs text-growth-dark">{topPick.score}% match</span>
          </div>
          <p className="mt-2 text-card-title">{topPick.title}</p>
          <p className="mt-1 text-sm text-ink-700">{topPick.reason}</p>
        </div>
      )}

      <div className="mt-10 grid gap-4 text-left sm:grid-cols-3">
        {tourSteps.map((step, i) => (
          <div key={step.title} className="rounded-xl2 border border-ink-700/10 bg-surface p-4">
            <span className="font-mono text-xs text-ink-700/60">0{i + 1}</span>
            <p className="mt-1 font-display text-base text-ink">{step.title}</p>
            <p className="mt-1 text-sm text-ink-700">{step.body}</p>
          </div>
        ))}
      </div>

      <button
        onClick={() => navigate("/skill-assessment")}
        className="mt-10 btn-primary"
      >
        Start with skill assessment
      </button>
    </div>
  );
}
