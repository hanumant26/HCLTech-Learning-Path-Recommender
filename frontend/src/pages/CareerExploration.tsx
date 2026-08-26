import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAsyncData } from "../hooks/useAsyncData";
import { getCareerCatalog, getProfile, saveProfile } from "../services/api";
import { useAuth } from "../hooks/useAuth";
import { CareerProfile } from "../types";
import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import Badge from "../components/common/Badge";
import ThemeToggle from "../components/common/ThemeToggle";
import { useToast } from "../hooks/useToast";

export default function CareerExploration() {
  const navigate = useNavigate();
  const { showToast } = useToast();
  const { user } = useAuth();
  const { data: careers, loading, error, reload } = useAsyncData(getCareerCatalog);
  const { data: profile } = useAsyncData(getProfile);

  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [settingGoal, setSettingGoal] = useState(false);

  if (loading) return <LoadingState label="Loading careers" />;
  if (error) return <ErrorState message={error} onRetry={reload} />;
  if (!careers) return null;

  const selected = careers.find((c) => c.id === selectedId) ?? careers[0];

  async function handleChoose(career: CareerProfile) {
    if (!user) {
      navigate("/signup", { state: { prefillCareerGoal: career.id } });
      return;
    }
    setSettingGoal(true);
    const base = profile ?? {
      id: "user-1",
      name: user.name,
      careerGoal: career.id,
      weeklyHours: 8,
      experienceLevel: "Beginner" as const,
    };
    await saveProfile({ ...base, careerGoal: career.id });
    setSettingGoal(false);
    showToast(`Career goal set to ${career.title}.`, "growth");
    navigate("/settings");
  }

  return (
    <div className="min-h-screen bg-paper">
      <header className="border-b border-ink-700/10 bg-paper/90 px-4 py-4">
        <div className="container-page flex items-center justify-between">
          <Link to={user ? "/profile" : "/"} className="text-brand">
            Pathfinder
          </Link>
          <div className="flex items-center gap-2">
            <ThemeToggle />
            {!user && (
              <>
                <Link
                  to="/login"
                  className="rounded-full border border-ink-700/20 px-4 py-1.5 text-sm text-ink transition hover:bg-ink-700/10"
                >
                  Sign in
                </Link>
                <Link
                  to="/signup"
                  className="rounded-full bg-ink px-4 py-1.5 text-sm text-paper transition hover:bg-ink-700"
                >
                  Get started
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      <div className="container-page page-shell">
        <h1 className="text-page-title">Explore careers</h1>
        <p className="text-page-subtitle">
          See what each path expects before you commit — required skills, target proficiency, and a
          rough timeframe from beginner.
        </p>

        <div className="mt-8 grid gap-6 lg:grid-cols-[280px_1fr]">
          <div className="flex gap-2 overflow-x-auto lg:flex-col lg:overflow-visible">
            {careers.map((c) => (
              <button
                key={c.id}
                onClick={() => setSelectedId(c.id)}
                className={`flex-none rounded-xl2 border px-4 py-3 text-left transition lg:flex-auto ${
                  selected.id === c.id
                    ? "border-growth bg-growth-light"
                    : "border-ink-700/10 bg-surface hover:border-ink-700/30"
                }`}
              >
                <p className="font-display text-base text-ink">{c.title}</p>
                <p className="mt-0.5 text-xs text-ink-700">{c.tagline}</p>
              </button>
            ))}
          </div>

          <div className="rounded-xl2 border border-ink-700/10 bg-surface p-6">
            <p className="font-display text-2xl text-ink">{selected.title}</p>
            <p className="mt-1 text-sm text-ink-700">{selected.tagline}</p>
            <p className="mt-4 text-sm text-ink-700">{selected.description}</p>

            <div className="mt-4">
              <Badge tone="amber">{selected.typicalTimeframe}</Badge>
            </div>

            <p className="mt-6 text-section-heading">Required skills</p>
            <div className="mt-3 space-y-3">
              {selected.requiredSkills.map((s) => (
                <div key={s.skillName}>
                  <div className="mb-1 flex items-center justify-between">
                    <span className="flex items-center gap-2 text-sm text-ink">
                      {s.skillName}
                      {s.core && <Badge tone="growth">Core</Badge>}
                    </span>
                    <span className="font-mono text-xs text-ink-700">{s.level}/5</span>
                  </div>
                  <div className="h-1.5 w-full overflow-hidden rounded-full bg-ink-700/10">
                    <div
                      className="h-full rounded-full bg-growth"
                      style={{ width: `${(s.level / 5) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={() => handleChoose(selected)}
              disabled={settingGoal}
              className="mt-8 btn-primary"
            >
              {settingGoal
                ? "Setting goal…"
                : user
                ? `Set as my goal`
                : `Sign up with ${selected.title} as my goal`}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
