import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAsyncData } from "../hooks/useAsyncData";
import { getCourseCatalog } from "../services/api";
import { ResourceType } from "../types";
import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import EmptyState from "../components/common/EmptyState";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import StarRating from "../components/common/StarRating";

type TypeFilter = "all" | ResourceType;
type DifficultyFilter = "all" | "Beginner" | "Intermediate" | "Advanced";

const typeTabs: { id: TypeFilter; label: string }[] = [
  { id: "all", label: "All types" },
  { id: "course", label: "Courses" },
  { id: "project", label: "Projects" },
  { id: "practice", label: "Practice" },
  { id: "assessment", label: "Assessments" },
];

const difficultyTabs: DifficultyFilter[] = ["all", "Beginner", "Intermediate", "Advanced"];

export default function CourseCatalog() {
  const navigate = useNavigate();
  const { data: courses, loading, error, reload } = useAsyncData(getCourseCatalog);

  const [query, setQuery] = useState("");
  const [typeFilter, setTypeFilter] = useState<TypeFilter>("all");
  const [difficultyFilter, setDifficultyFilter] = useState<DifficultyFilter>("all");
  const [skillFilter, setSkillFilter] = useState<string | null>(null);

  const allSkills = useMemo(() => {
    if (!courses) return [];
    const set = new Set<string>();
    courses.forEach((c) => c.skillsCovered.forEach((s) => set.add(s)));
    return Array.from(set).sort();
  }, [courses]);

  const filtered = useMemo(() => {
    if (!courses) return [];
    const q = query.trim().toLowerCase();
    return courses.filter((c) => {
      if (typeFilter !== "all" && c.type !== typeFilter) return false;
      if (difficultyFilter !== "all" && c.difficulty !== difficultyFilter) return false;
      if (skillFilter && !c.skillsCovered.includes(skillFilter)) return false;
      if (q && !c.title.toLowerCase().includes(q) && !c.description.toLowerCase().includes(q)) {
        return false;
      }
      return true;
    });
  }, [courses, query, typeFilter, difficultyFilter, skillFilter]);

  if (loading) return <LoadingState label="Loading the catalog" />;
  if (error) return <ErrorState message={error} onRetry={reload} />;

  function clearFilters() {
    setQuery("");
    setTypeFilter("all");
    setDifficultyFilter("all");
    setSkillFilter(null);
  }

  const hasActiveFilters =
    query !== "" || typeFilter !== "all" || difficultyFilter !== "all" || skillFilter !== null;

  return (
    <div className="container-page page-shell">
      <h1 className="text-page-title">Course catalog</h1>
      <p className="text-page-subtitle">
        Browse everything available, independent of your personal recommendations.
      </p>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search courses, projects, practice sets…"
        className="mt-6 w-full max-w-md rounded-xl2 border border-ink-700/20 bg-surface px-4 py-2.5 text-sm outline-none focus:border-growth"
      />

      <div className="mt-4 flex flex-wrap gap-2">
        {typeTabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setTypeFilter(t.id)}
            className={`rounded-full px-3.5 py-1.5 text-sm font-medium transition ${
              typeFilter === t.id ? "bg-ink text-paper" : "bg-ink-700/10 text-ink-700 hover:bg-ink-700/20"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="mt-2 flex flex-wrap gap-2">
        {difficultyTabs.map((d) => (
          <button
            key={d}
            onClick={() => setDifficultyFilter(d)}
            className={`rounded-full border px-3.5 py-1.5 text-sm font-medium transition ${
              difficultyFilter === d
                ? "border-growth bg-growth-light text-growth-dark"
                : "border-ink-700/20 text-ink-700 hover:bg-ink-700/10"
            }`}
          >
            {d === "all" ? "All levels" : d}
          </button>
        ))}
      </div>

      {allSkills.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1.5">
          {allSkills.map((s) => (
            <button
              key={s}
              onClick={() => setSkillFilter(skillFilter === s ? null : s)}
              className={`rounded-full px-2.5 py-1 font-mono text-[11px] uppercase tracking-wide transition ${
                skillFilter === s ? "bg-amber text-white" : "bg-amber-light text-amber hover:opacity-80"
              }`}
            >
              {s}
            </button>
          ))}
        </div>
      )}

      <p className="mt-4 text-xs text-ink-700">
        {filtered.length} of {courses?.length ?? 0} resources
        {hasActiveFilters && (
          <button onClick={clearFilters} className="ml-2 underline decoration-dotted hover:text-ink">
            Clear filters
          </button>
        )}
      </p>

      {filtered.length === 0 ? (
        <div className="mt-8">
          <EmptyState
            title="No matches"
            description="Try a different search term or clear your filters."
            action={{ label: "Clear filters", onClick: clearFilters }}
          />
        </div>
      ) : (
        <div className="mt-6 grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filtered.map((c) => (
            <Card key={c.id} onClick={() => navigate(`/resource/${c.id}`)}>
              <div className="mb-2 flex flex-wrap items-center gap-2">
                <Badge>{c.type}</Badge>
                <Badge>{c.difficulty}</Badge>
              </div>
              <p className="text-card-title">{c.title}</p>
              <p className="mt-1.5 line-clamp-2 text-sm text-ink-700">{c.description}</p>
              <div className="mt-3 flex flex-wrap gap-1.5">
                {c.skillsCovered.map((s) => (
                  <span key={s} className="rounded-full bg-ink-700/10 px-2 py-0.5 text-[11px] text-ink-700">
                    {s}
                  </span>
                ))}
              </div>
              <div className="mt-3 flex items-center justify-between">
                <StarRating rating={c.rating} />
                <span className="font-mono text-xs text-ink-700/70">{c.estimatedHours} hrs</span>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
