import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { LearnerProfile, CareerGoal } from "../types";
import { saveProfile } from "../services/api";
import { careerOptions, mockProfile } from "../data/mockData";
import { useAuth } from "../hooks/useAuth";

export default function Onboarding() {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();

  // If Signup collected a career goal already, skip the free-text intake
  // and go straight to the details step, pre-filled.
  const prefillGoal = (location.state as { prefillCareerGoal?: CareerGoal })?.prefillCareerGoal;

  const [goalText, setGoalText] = useState("");
  const [parsing, setParsing] = useState(false);
  const [form, setForm] = useState<LearnerProfile>({
    ...mockProfile,
    name: user?.name ?? mockProfile.name,
    careerGoal: prefillGoal ?? mockProfile.careerGoal,
  });
  const [saving, setSaving] = useState(false);
  const [step, setStep] = useState<"intake" | "details">(prefillGoal ? "details" : "intake");

  // Simulates the backend call to the Gemini API that parses free text
  // into a structured career goal. Replace with a real call to
  // services/api.ts once the endpoint exists.
  function handleParseGoal() {
    if (!goalText.trim()) return;
    setParsing(true);
    setTimeout(() => {
      const matched = careerOptions.find((c) =>
        goalText.toLowerCase().includes(c.toLowerCase().split(" ")[0])
      );
      setForm((f) => ({ ...f, careerGoal: (matched as CareerGoal) ?? f.careerGoal }));
      setParsing(false);
      setStep("details");
    }, 900);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSaving(true);
    await saveProfile(form);
    setSaving(false);
    navigate("/welcome");
  }

  return (
    <div className="container-narrow page-shell">
      <h1 className="text-page-title">Let's set up your profile</h1>
      <p className="text-page-subtitle">
        Tell us where you want to go, and we'll figure out the shape of the path.
      </p>

      {step === "intake" && (
        <div className="mt-8 rounded-xl2 border border-ink-700/10 bg-surface p-6">
          <label className="mb-2 block font-display text-lg text-ink">
            What's your learning goal?
          </label>
          <textarea
            value={goalText}
            onChange={(e) => setGoalText(e.target.value)}
            rows={3}
            placeholder="e.g. I want to become a Data Scientist within 6 months, coming from a non-technical background."
            className="input-field"
          />
          <button
            onClick={handleParseGoal}
            disabled={!goalText.trim() || parsing}
            className="mt-4 btn-primary"
          >
            {parsing ? "Analyzing your goal…" : "Continue"}
          </button>
        </div>
      )}

      {step === "details" && (
        <form onSubmit={handleSubmit} className="mt-8 space-y-5 rounded-xl2 border border-ink-700/10 bg-surface p-6">
          <div>
            <label className="form-label">Your name</label>
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              className="input-field"
              required
            />
          </div>

          <div>
            <label className="form-label">Target career</label>
            <select
              value={form.careerGoal}
              onChange={(e) => setForm({ ...form, careerGoal: e.target.value as CareerGoal })}
              className="input-field"
            >
              {careerOptions.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="form-label">Weekly hours</label>
              <input
                type="number"
                min={1}
                max={40}
                value={form.weeklyHours}
                onChange={(e) => setForm({ ...form, weeklyHours: Number(e.target.value) })}
                className="input-field"
              />
            </div>
            <div>
              <label className="form-label">Experience level</label>
              <select
                value={form.experienceLevel}
                onChange={(e) =>
                  setForm({ ...form, experienceLevel: e.target.value as LearnerProfile["experienceLevel"] })
                }
                className="input-field"
              >
                <option>Beginner</option>
                <option>Intermediate</option>
                <option>Advanced</option>
              </select>
            </div>
          </div>

          <div>
            <label className="form-label">
              Preferences <span className="text-ink-700/60">(optional)</span>
            </label>
            <input
              value={form.preferences ?? ""}
              onChange={(e) => setForm({ ...form, preferences: e.target.value })}
              placeholder="e.g. prefer hands-on projects over lectures"
              className="input-field"
            />
          </div>

          <button
            type="submit"
            disabled={saving}
            className="btn-primary"
          >
            {saving ? "Saving…" : "Save & continue"}
          </button>
        </form>
      )}
    </div>
  );
}
