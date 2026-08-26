import { ReactNode } from "react";
import { Link } from "react-router-dom";
import ThemeToggle from "../common/ThemeToggle";

const valueProps = [
  "A roadmap built around your real skill gaps, not a generic course list",
  "Everything ordered by prerequisite, so you never learn things out of order",
  "Progress tracking and feedback that actually reshapes your path",
];

interface AuthLayoutProps {
  children: ReactNode;
}

export default function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      {/* Branding panel — hidden below lg, where the form takes the full
          viewport instead. */}
      <div className="relative hidden flex-col justify-between bg-ink px-12 py-12 text-paper lg:flex xl:px-16 xl:py-16">
        <Link to="/" className="font-display text-2xl font-semibold tracking-tight text-paper">
          Pathfinder
        </Link>

        <div className="max-w-md">
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-paper/50">
            AI-Powered Learning
          </p>
          <h2 className="mt-5 font-display text-[2.5rem] font-semibold leading-[1.15] text-paper">
            Your personalized learning journey starts here.
          </h2>
          <ul className="mt-9 space-y-5">
            {valueProps.map((item) => (
              <li key={item} className="flex items-start gap-3 text-[17px] leading-relaxed text-paper/80">
                <span className="mt-2 h-1.5 w-1.5 flex-none rounded-full bg-growth" />
                {item}
              </li>
            ))}
          </ul>
        </div>

        <p className="text-sm text-paper/40">© {new Date().getFullYear()} Pathfinder</p>
      </div>

      {/* Form panel */}
      <div className="relative flex items-center justify-center bg-paper px-6 py-16 sm:px-12">
        <div className="absolute right-6 top-6 lg:right-10 lg:top-10">
          <ThemeToggle />
        </div>

        <div className="w-full max-w-md">
          <Link to="/" className="text-brand lg:hidden">
            Pathfinder
          </Link>
          {children}
        </div>
      </div>
    </div>
  );
}
