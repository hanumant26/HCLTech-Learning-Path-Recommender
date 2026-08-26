import { RoadmapNode } from "../../types";
import Badge from "../common/Badge";

interface RoadmapStepProps {
  node: RoadmapNode;
  isLast: boolean;
  onSelect: (node: RoadmapNode) => void;
}

const statusStyles: Record<RoadmapNode["status"], { dot: string; ring: string; label: string; tone: "growth" | "amber" | "neutral" }> = {
  completed: { dot: "bg-growth", ring: "ring-growth/30", label: "Completed", tone: "growth" },
  ready: { dot: "bg-amber", ring: "ring-amber/30", label: "Ready", tone: "amber" },
  locked: { dot: "bg-ink-700/30", ring: "ring-ink-700/10", label: "Locked", tone: "neutral" },
};

export default function RoadmapStep({ node, isLast, onSelect }: RoadmapStepProps) {
  const style = statusStyles[node.status];
  const isLocked = node.status === "locked";

  return (
    <li className="relative flex gap-4 pb-8">
      {!isLast && (
        <span
          className="absolute left-[15px] top-8 h-full w-px bg-ink-700/15"
          aria-hidden="true"
        />
      )}
      <span
        className={`relative z-10 mt-1 flex h-8 w-8 flex-none items-center justify-center rounded-full ring-4 ${style.ring} ${style.dot}`}
      >
        {node.status === "completed" && <span className="text-xs text-white">✓</span>}
        {node.status === "locked" && <span className="text-xs text-white">🔒</span>}
      </span>

      <button
        onClick={() => onSelect(node)}
        disabled={isLocked}
        className={`flex-1 rounded-xl2 border border-ink-700/10 bg-surface p-4 text-left shadow-sm transition ${
          isLocked ? "cursor-not-allowed opacity-70" : "hover:-translate-y-0.5 hover:shadow-md"
        }`}
      >
        <div className="mb-1.5 flex flex-wrap items-center gap-2">
          <Badge tone={style.tone}>{style.label}</Badge>
          <Badge>{node.type}</Badge>
          <Badge>{node.difficulty}</Badge>
          <span className="ml-auto font-mono text-xs text-ink-700">{node.estimatedHours} hrs</span>
        </div>
        <p className="font-display text-base font-medium text-ink">{node.title}</p>
        {isLocked && node.missingPrerequisites.length > 0 && (
          <p className="mt-1 text-xs text-clay">
            Requires: {node.missingPrerequisites.join(", ")}
          </p>
        )}
        {!isLocked && (
          <span className="mt-2 inline-block text-xs font-medium text-growth-dark">
            {node.status === "completed" ? "Review →" : "Start →"}
          </span>
        )}
      </button>
    </li>
  );
}
