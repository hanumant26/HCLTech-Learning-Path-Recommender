import { useNavigate, Link } from "react-router-dom";

const features = [
  {
    title: "Describe your goal",
    body: "Tell us your target role in plain language — the assistant parses it into a structured skill target.",
  },
  {
    title: "See your real gaps",
    body: "A side-by-side view of what the role needs versus what you already have.",
  },
  {
    title: "Follow a real sequence",
    body: "A prerequisite-aware roadmap, not just a pile of unordered course links.",
  },
  {
    title: "Adapt as you go",
    body: "Feedback on each step reshapes the path — too easy, too hard, or not relevant.",
  },
];

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="container-page py-16 sm:py-24">
      <div className="mx-auto max-w-2xl text-center">
        <p className="mb-4 font-mono text-xs uppercase tracking-[0.2em] text-growth-dark">
          AI-Powered Learning
        </p>
        <h1 className="font-display text-4xl font-semibold leading-tight text-ink sm:text-5xl">
          A learning path built around where you actually are.
        </h1>
        <p className="mx-auto mt-5 max-w-xl text-base text-ink-700 sm:text-lg">
          Pathfinder turns a career goal and a skill snapshot into a milestone-driven roadmap —
          ordered by real prerequisites, explained in plain language, and adjusted as you learn.
        </p>
        <div className="mt-8 flex items-center justify-center gap-3">
          <button
            onClick={() => navigate("/signup")}
            className="btn-primary"
          >
            Get Started
          </button>
          <button
            onClick={() => navigate("/login")}
            className="btn-secondary"
          >
            Sign in
          </button>
        </div>
        <p className="mt-4 text-sm text-ink-700">
          Not sure which career to aim for?{" "}
          <Link to="/careers" className="font-medium text-growth-dark hover:underline">
            Explore careers first
          </Link>
        </p>
      </div>

      <div className="mx-auto mt-20 grid max-w-3xl gap-6 sm:grid-cols-2">
        {features.map((f, i) => (
          <div key={f.title} className="rounded-xl2 border border-ink-700/10 bg-surface p-5">
            <span className="font-mono text-xs text-ink-700/60">0{i + 1}</span>
            <p className="mt-1 text-card-title">{f.title}</p>
            <p className="mt-1.5 text-sm text-ink-700">{f.body}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
