import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { getNotifications, markNotificationRead, markAllNotificationsRead } from "../../services/api";
import { NotificationItem, NotificationType } from "../../types";

const iconFor: Record<NotificationType, string> = {
  new_recommendation: "✨",
  milestone_unlocked: "🔓",
  path_adjusted: "🔄",
};

function timeAgo(iso: string): string {
  const diffMs = Date.now() - new Date(iso).getTime();
  const hours = Math.floor(diffMs / (1000 * 60 * 60));
  if (hours < 1) return "Just now";
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

export default function NotificationsBell() {
  const [open, setOpen] = useState(false);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [loading, setLoading] = useState(true);
  const containerRef = useRef<HTMLDivElement>(null);

  const unreadCount = notifications.filter((n) => !n.read).length;

  useEffect(() => {
    getNotifications()
      .then(setNotifications)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  async function handleOpen() {
    setOpen((o) => !o);
  }

  async function handleItemClick(item: NotificationItem) {
    if (!item.read) {
      await markNotificationRead(item.id);
      setNotifications((prev) => prev.map((n) => (n.id === item.id ? { ...n, read: true } : n)));
    }
    setOpen(false);
  }

  async function handleMarkAllRead() {
    await markAllNotificationsRead();
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  }

  return (
    <div ref={containerRef} className="relative">
      <button
        onClick={handleOpen}
        aria-label="Notifications"
        className="relative flex h-10 w-10 items-center justify-center rounded-full border border-ink-700/20 text-sm text-ink-700 transition hover:bg-ink-700/10"
      >
        🔔
        {unreadCount > 0 && (
          <span className="absolute -right-1 -top-1 flex h-4 min-w-4 items-center justify-center rounded-full bg-clay px-1 font-mono text-[10px] text-white">
            {unreadCount > 9 ? "9+" : unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 z-50 mt-2 w-80 overflow-hidden rounded-xl2 border border-ink-700/10 bg-surface shadow-xl sm:w-96">
          <div className="flex items-center justify-between border-b border-ink-700/10 px-4 py-3">
            <p className="font-display text-sm font-medium text-ink">Notifications</p>
            {unreadCount > 0 && (
              <button
                onClick={handleMarkAllRead}
                className="text-xs text-ink-700 underline decoration-dotted hover:text-ink"
              >
                Mark all read
              </button>
            )}
          </div>

          <div className="max-h-96 overflow-y-auto">
            {loading ? (
              <p className="px-4 py-6 text-center text-sm text-ink-700">Loading…</p>
            ) : notifications.length === 0 ? (
              <p className="px-4 py-6 text-center text-sm text-ink-700">You're all caught up.</p>
            ) : (
              notifications.map((n) => (
                <Link
                  key={n.id}
                  to={n.linkTo ?? "#"}
                  onClick={() => handleItemClick(n)}
                  className={`flex gap-3 border-b border-ink-700/5 px-4 py-3 text-left transition hover:bg-ink-700/5 ${
                    !n.read ? "bg-growth-light/40" : ""
                  }`}
                >
                  <span className="text-base" aria-hidden="true">
                    {iconFor[n.type]}
                  </span>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-1.5">
                      <p className="text-sm font-medium text-ink">{n.title}</p>
                      {!n.read && <span className="h-1.5 w-1.5 flex-none rounded-full bg-growth" />}
                    </div>
                    <p className="mt-0.5 text-xs text-ink-700">{n.body}</p>
                    <p className="mt-1 font-mono text-[11px] text-ink-700/60">{timeAgo(n.timestamp)}</p>
                  </div>
                </Link>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
