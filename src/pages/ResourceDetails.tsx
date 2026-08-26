import { useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useAsyncData } from "../hooks/useAsyncData";
import { getRecommendations, getRoadmap, getCourseCatalog, submitFeedback } from "../services/api";
import { FeedbackValue } from "../types";
import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import EmptyState from "../components/common/EmptyState";
import Badge from "../components/common/Badge";
import StarRating from "../components/common/StarRating";
import { useToast } from "../hooks/useToast";

const feedbackOptions: { value: FeedbackValue; label: string }[] = [
  { value: "too_easy", label: "Too easy" },
  { value: "appropriate", label: "Appropriate" },
  { value: "too_difficult", label: "Too difficult" },
  { value: "not_relevant", label: "Not relevant" },
];

export default function ResourceDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const { data: recs, loading: loadingRecs } = useAsyncData(getRecommendations);
  const { data: roadmap, loading: loadingRoadmap } = useAsyncData(getRoadmap);
  const { data: catalog, loading: loadingCatalog } = useAsyncData(getCourseCatalog);
  const [status, setStatus] = useState<"not_started" | "in_progress" | "complete">("not_started");
  const [feedbackSent, setFeedbackSent] = useState<FeedbackValue | null>(null);
  const [sendingFeedback, setSendingFeedback] = useState(false);

  const loading = loadingRecs || loadingRoadmap || loadingCatalog;

  if (loading) return <LoadingState label="Loading resource" />;

  const resource = recs?.find((r) => r.id === id);
  const roadmapNode = roadmap?.find((n) => n.id === id);
  const catalogCourse = catalog?.find((c) => c.id === id);

  if (!resource && !roadmapNode && !catalogCourse) {
    return (
      <div className="container-page py-12">
        <EmptyState
          title="Resource not found"
          description="It may have been removed or the link is out of date."
          action={{ label: "Browse the catalog", onClick: () => navigate("/courses") }}
        />
      </div>
    );
  }

  const title = resource?.title ?? roadmapNode?.title ?? catalogCourse?.title ?? "";
  const type = resource?.type ?? roadmapNode?.type ?? catalogCourse?.type ?? "course";
  const difficulty = resource?.difficulty ?? roadmapNode?.difficulty ?? catalogCourse?.difficulty ?? "Beginner";
  const hours = resource?.estimatedHours ?? roadmapNode?.estimatedHours ?? catalogCourse?.estimatedHours ?? 0;
  const description = resource?.description ?? catalogCourse?.description;
  const skillsCovered = resource?.skillsCovered ?? catalogCourse?.skillsCovered ?? [];

  async function handleFeedback(value: FeedbackValue) {
    if (!id) return;
    setSendingFeedback(true);
    await submitFeedback(id, value);
    setFeedbackSent(value);
    setSendingFeedback(false);
    showToast("Thanks — your path will adjust if needed.", "growth");
  }

  return (
    <div className="container-narrow page-shell">
      <Link to="/recommendations" className="text-sm text-ink-700 hover:text-ink">
        ← Back
      </Link>

      <div className="mt-4 flex flex-wrap items-center gap-2">
        <Badge>{type}</Badge>
        <Badge>{difficulty}</Badge>
        <span className="font-mono text-xs text-ink-700">{hours} hrs</span>
      </div>

      <h1 className="mt-3 text-page-title">{title}</h1>

      {catalogCourse && !resource && (
        <div className="mt-2">
          <StarRating rating={catalogCourse.rating} />
        </div>
      )}

      {description && <p className="mt-4 text-ink-700">{description}</p>}

      {resource && (
        <>
          <div className="mt-6 rounded-xl2 border border-growth/30 bg-growth-light p-4">
            <p className="font-mono text-xs uppercase tracking-wide text-growth-dark">
              Why this was recommended
            </p>
            <p className="mt-1 text-sm text-ink">{resource.reason}</p>
          </div>

          {resource.prerequisites.length > 0 && (
            <div className="mt-4">
              <p className="text-sm font-medium text-ink">Prerequisites</p>
              <ul className="mt-1 list-inside list-disc text-sm text-ink-700">
                {resource.prerequisites.map((p) => (
                  <li key={p}>{p}</li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}

      {skillsCovered.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-1.5">
          {skillsCovered.map((s) => (
            <span key={s} className="rounded-full bg-ink-700/10 px-2.5 py-1 text-xs text-ink-700">
              {s}
            </span>
          ))}
        </div>
      )}

      <div className="mt-8 flex gap-3">
        {type === "assessment" ? (
          <Link
            to={`/assessment/${id}`}
            className="btn-primary"
          >
            Take assessment
          </Link>
        ) : (
          <>
            {status !== "complete" && (
              <button
                onClick={() => setStatus(status === "not_started" ? "in_progress" : "complete")}
                className="btn-primary"
              >
                {status === "not_started" ? "Start" : "Mark complete"}
              </button>
            )}
            {status === "complete" && <Badge tone="growth">Completed</Badge>}
          </>
        )}
      </div>

      {status === "complete" && type !== "assessment" && (
        <div className="mt-8 rounded-xl2 border border-ink-700/10 bg-surface p-5">
          <p className="font-display text-base text-ink">How was this?</p>
          {feedbackSent ? (
            <p className="mt-2 text-sm text-growth-dark">
              Thanks — your path will adjust if needed.
            </p>
          ) : (
            <div className="mt-3 flex flex-wrap gap-2">
              {feedbackOptions.map((opt) => (
                <button
                  key={opt.value}
                  onClick={() => handleFeedback(opt.value)}
                  disabled={sendingFeedback}
                  className="rounded-full border border-ink-700/20 px-3.5 py-1.5 text-sm text-ink-700 transition hover:bg-ink-700/10 disabled:opacity-50"
                >
                  {opt.label}
                </button>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
