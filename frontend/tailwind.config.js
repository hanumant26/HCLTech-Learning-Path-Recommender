/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // "Study atlas" palette — deep indigo ink, warm paper, forest-growth
        // accent. Values are CSS custom properties so the whole palette can
        // flip for dark mode (see index.css) without touching component
        // files — every page already uses these token names.
        ink: {
          DEFAULT: "rgb(var(--color-ink) / <alpha-value>)",
          800: "rgb(var(--color-ink-800) / <alpha-value>)",
          700: "rgb(var(--color-ink-700) / <alpha-value>)",
          600: "rgb(var(--color-ink-600) / <alpha-value>)",
        },
        paper: {
          DEFAULT: "rgb(var(--color-paper) / <alpha-value>)",
          dim: "rgb(var(--color-paper-dim) / <alpha-value>)",
        },
        surface: "rgb(var(--color-surface) / <alpha-value>)",
        growth: {
          DEFAULT: "rgb(var(--color-growth) / <alpha-value>)",
          light: "rgb(var(--color-growth-light) / <alpha-value>)",
          dark: "rgb(var(--color-growth-dark) / <alpha-value>)",
        },
        amber: {
          DEFAULT: "rgb(var(--color-amber) / <alpha-value>)",
          light: "rgb(var(--color-amber-light) / <alpha-value>)",
        },
        clay: {
          DEFAULT: "rgb(var(--color-clay) / <alpha-value>)",
          light: "rgb(var(--color-clay-light) / <alpha-value>)",
        },
      },
      fontFamily: {
        display: ["'Fraunces'", "ui-serif", "Georgia", "serif"],
        body: ["'Inter'", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "ui-monospace", "monospace"],
      },
      borderRadius: {
        xl2: "1.25rem",
      },
    },
  },
  plugins: [],
};
