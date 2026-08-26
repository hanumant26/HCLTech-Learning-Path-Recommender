import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import ThemeToggle from "../common/ThemeToggle";
import NotificationsBell from "./NotificationsBell";
import NavMoreMenu from "./NavMoreMenu";
import MobileNavMenu from "./MobileNavMenu";

const primaryNavItems = [
  { to: "/profile", label: "My Profile", end: true },
  { to: "/skill-assessment", label: "Skill Assessment" },
  { to: "/recommendations", label: "Recommendations" },
  { to: "/courses", label: "Browse Courses" },
  { to: "/roadmap", label: "Roadmap" },
  { to: "/progress", label: "Progress" },
];

const secondaryNavItems = [
  { to: "/activity", label: "Activity" },
  { to: "/achievements", label: "Achievements" },
  { to: "/careers", label: "Careers" },
];

const allNavItems = [...primaryNavItems, ...secondaryNavItems];

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  `whitespace-nowrap rounded-full px-5 py-2.5 text-[15px] font-medium transition ${
    isActive ? "bg-ink text-paper" : "text-ink-700 hover:bg-ink-700/10"
  }`;

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <header className="sticky top-0 z-40 border-b border-ink-700/10 bg-paper/95 backdrop-blur">
      {/* Brand | Main Navigation | Secondary Actions — three conceptual
          groups rather than one packed row, each with its own breathing
          room via gap-8 between groups. */}
      <div className="container-page flex h-20 items-center justify-between gap-8">
        <NavLink to="/profile" className="flex-none text-brand">
          Pathfinder
        </NavLink>

        <nav className="hidden flex-1 items-center gap-2 lg:flex">
          {primaryNavItems.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.end} className={navLinkClass}>
              {item.label}
            </NavLink>
          ))}
          <NavMoreMenu items={secondaryNavItems} />
        </nav>

        <div className="flex flex-none items-center gap-3">
          {user && (
            <span className="hidden whitespace-nowrap text-[15px] text-ink-700 xl:inline">
              {user.name}
            </span>
          )}

          <div className="hidden items-center gap-2 border-l border-ink-700/10 pl-4 lg:flex">
            <ThemeToggle />
            <NotificationsBell />
            <NavLink
              to="/settings"
              aria-label="Settings"
              className={({ isActive }) =>
                `flex h-10 w-10 items-center justify-center rounded-full border text-base transition ${
                  isActive
                    ? "border-ink bg-ink text-paper"
                    : "border-ink-700/20 text-ink-700 hover:bg-ink-700/10"
                }`
              }
            >
              ⚙
            </NavLink>
            <button
              onClick={handleLogout}
              className="btn-secondary"
            >
              Log out
            </button>
          </div>

          <div className="flex items-center gap-2 lg:hidden">
            <NotificationsBell />
            <MobileNavMenu items={allNavItems} />
          </div>
        </div>
      </div>
    </header>
  );
}
