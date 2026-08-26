import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { careerOptions } from "../data/mockData";
import { CareerGoal } from "../types";
import AuthLayout from "../components/layout/AuthLayout";

function passwordStrength(pw: string): { label: string; tone: string; percent: number } {
  if (pw.length === 0) return { label: "", tone: "bg-transparent", percent: 0 };
  if (pw.length < 6) return { label: "Too short", tone: "bg-clay", percent: 25 };
  if (pw.length < 10) return { label: "Okay", tone: "bg-amber", percent: 60 };
  return { label: "Strong", tone: "bg-growth", percent: 100 };
}

export default function Signup() {
  const { signup } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const incomingGoal = (location.state as { prefillCareerGoal?: CareerGoal })?.prefillCareerGoal;

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [careerGoal, setCareerGoal] = useState(incomingGoal ?? "");
  const [agreed, setAgreed] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const strength = passwordStrength(password);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    if (password !== confirm) {
      setError("Passwords don't match.");
      return;
    }
    if (!agreed) {
      setError("Please accept the terms to continue.");
      return;
    }

    setSubmitting(true);
    try {
      await signup(name, email, password);
      // If they picked a goal here, skip straight past the intake step —
      // Onboarding can read this from navigation state and pre-fill.
      navigate("/profile", { state: { prefillCareerGoal: careerGoal || undefined } });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthLayout>
      <h1 className="mt-8 text-section-heading lg:mt-0">Create your account</h1>
      <p className="mt-2 text-[15px] leading-relaxed text-ink-700">
        Takes under a minute — the rest is guided.
      </p>

      <form onSubmit={handleSubmit} className="mt-8 space-y-5">
        {error && (
          <p className="rounded-xl2 border border-clay/30 bg-clay-light px-4 py-3 text-[15px] text-clay">
            {error}
          </p>
        )}

        <div>
          <label className="form-label">Full name</label>
          <input
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Aditi Sharma"
            className="input-field bg-surface"
          />
        </div>

        <div>
          <label className="form-label">Email</label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="input-field bg-surface"
          />
        </div>

        <div>
          <label className="form-label">Password</label>
          <input
            type="password"
            required
            minLength={6}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="input-field bg-surface"
          />
          {password && (
            <div className="mt-2">
              <div className="h-1.5 w-full overflow-hidden rounded-full bg-ink-700/10">
                <div
                  className={`h-full rounded-full transition-all ${strength.tone}`}
                  style={{ width: `${strength.percent}%` }}
                />
              </div>
              <p className="mt-1.5 text-sm text-ink-700">{strength.label}</p>
            </div>
          )}
        </div>

        <div>
          <label className="form-label">Confirm password</label>
          <input
            type="password"
            required
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            placeholder="••••••••"
            className="input-field bg-surface"
          />
        </div>

        <div>
          <label className="form-label">
            Career goal <span className="text-ink-700/60">(optional — you can set this later)</span>
          </label>
          <select
            value={careerGoal}
            onChange={(e) => setCareerGoal(e.target.value)}
            className="input-field bg-surface"
          >
            <option value="">I'll decide later</option>
            {careerOptions.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
          {incomingGoal && (
            <p className="mt-1.5 text-sm text-growth-dark">
              Pre-filled from Explore Careers — change it anytime.
            </p>
          )}
        </div>

        <label className="flex items-start gap-2.5 text-[15px] text-ink-700">
          <input
            type="checkbox"
            checked={agreed}
            onChange={(e) => setAgreed(e.target.checked)}
            className="mt-0.5 h-4 w-4 accent-growth"
          />
          <span>I agree to the Terms of Service and Privacy Policy.</span>
        </label>

        <button type="submit" disabled={submitting} className="w-full btn-primary">
          {submitting ? "Creating account…" : "Create account"}
        </button>
      </form>

      <p className="mt-8 text-center text-[15px] text-ink-700">
        Already have an account?{" "}
        <Link to="/login" className="font-medium text-growth-dark hover:underline">
          Sign in
        </Link>
      </p>
    </AuthLayout>
  );
}
