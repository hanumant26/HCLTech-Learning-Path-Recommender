import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAsyncData } from "../hooks/useAsyncData";
import { getSkills } from "../services/api";
import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import EmptyState from "../components/common/EmptyState";
import Badge from "../components/common/Badge";

export default function SkillAssessment() {
  const navigate = useNavigate();
  const { data: skills, loading, error, reload } = useAsyncData(getSkills);
  const [levels, setLevels] = useState<Record<string, number>>({});

  function currentLevel(skillId: string, fallback: number) {
    return levels[skillId] ?? fallback;
  }

  if (loading) return <LoadingState label="Loading your skills" />;
  if (error) return <ErrorState message={error} onRetry={reload} />;
  if (!skills || skills.length === 0)
    return (
      <EmptyState
        title="No skills recorded yet"
        description="Complete your profile first so we know what to assess."
        action={{ label: "Go to profile", onClick: () => navigate("/profile") }}
      />
    );

  return (
    <div className="container-page page-shell">
      <div className="page-header">
        <h1 className="text-page-title">Skill assessment</h1>
        <p className="text-page-subtitle">
          Rate your current proficiency in each skill. The marker on the bar shows the level your
          target career expects.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {skills.map((s) => {
          const level = currentLevel(s.skillId, s.proficiency);
          const required = s.requiredForGoal ?? level;
          const gap = required - level;

          return (
            <div key={s.skillId} className="rounded-xl2 border border-ink-700/10 bg-surface p-8">
              {/* Skill name → current level */}
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-card-title">{s.skillName}</p>
                  <p className="mt-1.5 text-supporting">Current proficiency</p>
                </div>
                <div className="flex-none text-right">
                  <p className="font-mono text-4xl font-semibold leading-none text-ink">
                    {level}
                    <span className="text-xl font-normal text-ink-700">/5</span>
                  </p>
                </div>
              </div>

              {/* Progress indicator with target marker */}
              <div className="mt-7">
                <div className="relative h-3 w-full rounded-full bg-ink-700/10 shadow-inner">
                  <div
                    className="h-3 rounded-full bg-growth transition-all duration-300"
                    style={{ width: `${(level / 5) * 100}%` }}
                  />
                  <div
                    className="absolute top-1/2 h-5 w-1 -translate-y-1/2 rounded-full bg-ink-800"
                    style={{ left: `calc(${(required / 5) * 100}% - 2px)` }}
                    title={`Target: ${required}/5`}
                  />
                </div>
                <input
                  type="range"
                  min={1}
                  max={5}
                  value={level}
                  onChange={(e) =>
                    setLevels((prev) => ({ ...prev, [s.skillId]: Number(e.target.value) }))
                  }
                  className="mt-4 w-full accent-growth"
                  aria-label={`${s.skillName} proficiency`}
                />
              </div>

              {/* Target level + supporting info */}
              <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t border-ink-700/10 pt-6">
                <p className="text-supporting">
                  Target for your goal: <span className="font-mono font-medium text-ink">{required}/5</span>
                </p>
                {gap > 0 ? (
                  <Badge tone="amber">
                    {gap} level{gap > 1 ? "s" : ""} to go
                  </Badge>
                ) : (
                  <Badge tone="growth">Target met</Badge>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <button
        onClick={() => navigate("/recommendations")}
        className="section-spacing btn-primary"
      >
        See my recommendations
      </button>
    </div>
  );
}
