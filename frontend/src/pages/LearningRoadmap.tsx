import { useNavigate } from "react-router-dom";
import { useAsyncData } from "../hooks/useAsyncData";
import { getRoadmap } from "../services/api";
import { RoadmapNode } from "../types";
import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import EmptyState from "../components/common/EmptyState";
import RoadmapStep from "../components/roadmap/RoadmapStep";

export default function LearningRoadmap() {
  const navigate = useNavigate();
  const { data: nodes, loading, error, reload } = useAsyncData(getRoadmap);

  if (loading) return <LoadingState label="Building your roadmap" />;
  if (error) return <ErrorState message={error} onRetry={reload} />;
  if (!nodes || nodes.length === 0)
    return (
      <div className="container-page py-12">
        <EmptyState
          title="No roadmap yet"
          description="Finish your skill assessment so we can generate an ordered path."
          action={{ label: "Go to skill assessment", onClick: () => navigate("/skill-assessment") }}
        />
      </div>
    );

  const sorted = [...nodes].sort((a, b) => a.order - b.order);

  function handleSelect(node: RoadmapNode) {
    navigate(`/resource/${node.id}`);
  }

  return (
    <div className="container-narrow page-shell">
      <h1 className="text-page-title">Your learning roadmap</h1>
      <p className="text-page-subtitle">
        Ordered by prerequisite. Locked steps unlock automatically once you complete what they depend on.
      </p>

      <ol className="mt-8">
        {sorted.map((node, i) => (
          <RoadmapStep
            key={node.id}
            node={node}
            isLast={i === sorted.length - 1}
            onSelect={handleSelect}
          />
        ))}
      </ol>
    </div>
  );
}
