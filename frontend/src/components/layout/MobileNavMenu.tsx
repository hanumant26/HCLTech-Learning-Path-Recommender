import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import ThemeToggle from "../common/ThemeToggle";

interface MobileNavMenuProps {
  items: { to: string; label: string; end?: boolean }[];
}

export default function MobileNavMenu({ items }: MobileNavMenuProps) {
  const [open, setOpen] = useState(false);
  const { logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    setOpen(false);
    logout();
    navigate("/login");
  }

  return (
    <div className="lg:hidden">
      <button
        onClick={() => setOpen((o) => !o)}
        aria-label="Toggle menu"
        aria-expanded={open}
        className="flex h-10 w-10 items-center justify-center rounded-full border border-ink-700/20 text-ink-700 transition hover:bg-ink-700/10"
      >
        {open ? "✕" : "☰"}
      </button>

      {open && (
        <div className="fixed inset-x-0 top-20 z-40 max-h-[calc(100vh-5rem)] overflow-y-auto border-b border-ink-700/10 bg-paper px-5 py-5 shadow-lg">
          <nav className="flex flex-col gap-1">
            {items.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                onClick={() => setOpen(false)}
                className={({ isActive }) =>
                  `rounded-xl2 px-4 py-3 text-base font-medium transition ${
                    isActive ? "bg-ink text-paper" : "text-ink-700 hover:bg-ink-700/10"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div className="mt-4 flex items-center justify-between border-t border-ink-700/10 pt-4">
            <div className="flex items-center gap-3">
              <ThemeToggle />
              <NavLink
                to="/settings"
                onClick={() => setOpen(false)}
                className="rounded-full border border-ink-700/20 px-4 py-2 text-sm text-ink-700 transition hover:bg-ink-700/10"
              >
                ⚙ Settings
              </NavLink>
            </div>
            <button
              onClick={handleLogout}
              className="rounded-full border border-ink-700/20 px-4 py-2 text-sm text-ink-700 transition hover:bg-ink-700/10"
            >
              Log out
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
