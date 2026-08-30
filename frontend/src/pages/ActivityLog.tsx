import { useMemo, useState } from "react";
import { useAsyncData } from "../hooks/useAsyncData";
import { getActivityLog } from "../services/api";
import { ActivityEvent, ActivityEventType } from "../types";
import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import EmptyState from "../components/common/EmptyState";
import Badge from "../components/common/Badge";

type FilterTab = "all" | ActivityEventType;

const tabs: { id: FilterTab; label: string }[] = [
  { id: "all", label: "All activity" },
  { id: "resource_completed", label: "Completed" },
  { id: "feedback_given", label: "Feedback" },
  { id: "assessment_taken", label: "Assessments" },
];

const iconFor: Record<ActivityEventType, string> = {
  resource_completed: "✓",
  feedback_given: "💬",
  assessment_taken: "📝",
};

function toneFor(event: ActivityEvent): "growth" | "amber" | "clay" | "neutral" {
  if (event.type === "resource_completed") return "growth";
  if (event.type === "feedback_given") return "amber";
  if (event.type === "assessment_taken") {
    return event.detail?.toLowerCase().startsWith("passed") ? "growth" : "clay";
  }
  return "neutral";
}

function labelFor(type: ActivityEventType): string {
  if (type === "resource_completed") return "Completed";
  if (type === "feedback_given") return "Feedback";
  return "Assessment";
}

function dateGroupLabel(iso: string): string {
  const date = new Date(iso);
  const today = new Date();
  const yesterday = new Date();
  yesterday.setDate(today.getDate() - 1);

  const isSameDay = (a: Date, b: Date) =>
    a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();

  if (isSameDay(date, today)) return "Today";
  if (isSameDay(date, yesterday)) return "Yesterday";
  return date.toLocaleDateString(undefined, { month: "long", day: "numeric", year: "numeric" });
}

function timeLabel(iso: string): string {
  return new Date(iso).toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
}

export default function ActivityLog() {
  const { data: events, loading, error, reload } = useAsyncData(getActivityLog);
  const [tab, setTab] = useState<FilterTab>("all");

  const filtered = useMemo(
    () => (events ?? []).filter((e) => tab === "all" || e.type === tab),
    [events, tab]
  );

  const grouped = useMemo(() => {
    const groups: { label: string; events: ActivityEvent[] }[] = [];
    for (const event of filtered) {
      const label = dateGroupLabel(event.timestamp);
      const existing = groups.find((g) => g.label === label);
      if (existing) existing.events.push(event);
      else groups.push({ label, events: [event] });
    }
    return groups;
  }, [filtered]);

  if (loading) return <LoadingState label="Loading your activity" />;
  if (error) return <ErrorState message={error} onRetry={reload} />;

  return (
    <div className="container-narrow page-shell">
      <h1 className="text-page-title">Activity</h1>
      <p className="text-page-subtitle">Everything you've done, in order — separate from milestones.</p>

      <div className="mt-6 flex flex-wrap gap-2">
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`rounded-full px-3.5 py-1.5 text-sm font-medium transition ${
              tab === t.id ? "bg-ink text-paper" : "bg-ink-700/10 text-ink-700 hover:bg-ink-700/20"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {grouped.length === 0 ? (
        <div className="mt-8">
          <EmptyState title="Nothing here yet" description="Activity will show up as you complete resources, give feedback, and take assessments." />
        </div>
      ) : (
        <div className="mt-8 space-y-8">
          {grouped.map((group) => (
            <div key={group.label}>
              <p className="mb-3 font-mono text-xs uppercase tracking-wide text-ink-700/60">
                {group.label}
              </p>
              <ul className="space-y-2">
                {group.events.map((event) => (
                  <li
                    key={event.id}
                    className="flex items-start gap-3 rounded-xl2 border border-ink-700/10 bg-surface p-4"
                  >
                    <span className="mt-0.5 text-base" aria-hidden="true">
                      {iconFor[event.type]}
                    </span>
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <Badge tone={toneFor(event)}>{labelFor(event.type)}</Badge>
                        <span className="font-mono text-[11px] text-ink-700/60">
                          {timeLabel(event.timestamp)}
                        </span>
                      </div>
                      <p className="mt-1.5 font-display text-base text-ink">{event.title}</p>
                      {event.detail && <p className="mt-0.5 text-sm text-ink-700">{event.detail}</p>}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
