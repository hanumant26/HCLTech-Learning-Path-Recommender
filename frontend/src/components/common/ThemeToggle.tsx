import { useTheme } from "../../hooks/useTheme";

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      aria-label={theme === "light" ? "Switch to dark mode" : "Switch to light mode"}
      className="flex h-10 w-10 items-center justify-center rounded-full border border-ink-700/20 text-sm text-ink-700 transition hover:bg-ink-700/10"
    >
      {theme === "light" ? "🌙" : "☀️"}
    </button>
  );
}
