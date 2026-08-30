import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import AuthLayout from "../components/layout/AuthLayout";
import { useToast } from "../hooks/useToast";

export default function Login() {
  const { login, loginAsGuest } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from?: string })?.from ?? "/profile";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleGuest() {
    setSubmitting(true);
    await loginAsGuest();
    navigate("/profile", { replace: true });
  }

  return (
    <AuthLayout>
      <h1 className="mt-8 text-section-heading lg:mt-0">Welcome back</h1>
      <p className="mt-2 text-[15px] leading-relaxed text-ink-700">
        Sign in to pick up your learning path.
      </p>

      <form onSubmit={handleSubmit} className="mt-8 space-y-5">
        {error && (
          <p className="rounded-xl2 border border-clay/30 bg-clay-light px-4 py-3 text-[15px] text-clay">
            {error}
          </p>
        )}

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
          <div className="mb-2 flex items-center justify-between">
            <label className="text-[15px] font-medium text-ink">Password</label>
            <button
              type="button"
              onClick={() =>
                showToast(
                  "Password reset isn't wired up yet — placeholder for the real flow.",
                  "amber"
                )
              }
              className="text-sm text-ink-700 underline decoration-dotted hover:text-ink"
            >
              Forgot password?
            </button>
          </div>
          <input
            type="password"
            required
            minLength={6}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="input-field bg-surface"
          />
        </div>

        <label className="flex items-center gap-2.5 text-[15px] text-ink-700">
          <input
            type="checkbox"
            checked={remember}
            onChange={(e) => setRemember(e.target.checked)}
            className="h-4 w-4 accent-growth"
          />
          Remember me
        </label>

        <button type="submit" disabled={submitting} className="w-full btn-primary">
          {submitting ? "Signing in…" : "Sign in"}
        </button>
      </form>

      <div className="my-6 flex items-center gap-3">
        <span className="h-px flex-1 bg-ink-700/15" />
        <span className="text-sm text-ink-700/60">or</span>
        <span className="h-px flex-1 bg-ink-700/15" />
      </div>

      <button onClick={handleGuest} disabled={submitting} className="w-full btn-secondary">
        Continue as guest
      </button>

      <p className="mt-8 text-center text-[15px] text-ink-700">
        New here?{" "}
        <Link to="/signup" className="font-medium text-growth-dark hover:underline">
          Create an account
        </Link>
      </p>
    </AuthLayout>
  );
}
