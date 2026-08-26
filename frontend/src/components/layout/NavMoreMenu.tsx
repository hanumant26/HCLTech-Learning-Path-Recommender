import { useEffect, useRef, useState } from "react";
import { NavLink, useLocation } from "react-router-dom";

interface NavMoreMenuProps {
  items: { to: string; label: string }[];
}

export default function NavMoreMenu({ items }: NavMoreMenuProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const location = useLocation();

  const isAnyActive = items.some((item) => location.pathname === item.to);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen((o) => !o)}
        className={`whitespace-nowrap rounded-full px-5 py-2.5 text-[15px] font-medium transition ${
          isAnyActive ? "bg-ink text-paper" : "text-ink-700 hover:bg-ink-700/10"
        }`}
      >
        More ▾
      </button>

      {open && (
        <div className="absolute left-0 z-50 mt-2 w-52 overflow-hidden rounded-xl2 border border-ink-700/10 bg-surface py-2 shadow-xl">
          {items.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `block px-4 py-2.5 text-[15px] transition ${
                  isActive ? "bg-growth-light text-growth-dark" : "text-ink-700 hover:bg-ink-700/10"
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>
      )}
    </div>
  );
}
