"""
Prerequisite Engine Service.
Uses NetworkX DAG graph traversal and database relationships to check prerequisite satisfaction,
identify missing prerequisites, and resolve prerequisite chains for candidates and roadmap steps.
"""
from typing import Dict, List, Set, Any, Tuple
import networkx as nx
from sqlalchemy.orm import Session
from backend.app.models.skill import Skill, SkillPrerequisite


class PrerequisiteEngine:
    """Service to query, validate, and resolve skill prerequisites using NetworkX."""

    def __init__(self, db: Session):
        self.db = db
        self.dag = self._build_prerequisite_dag()

    def _build_prerequisite_dag(self) -> nx.DiGraph:
        """
        Build NetworkX DiGraph where edge (A -> B) means skill A is a prerequisite for skill B.
        """
        graph = nx.DiGraph()
        skills = self.db.query(Skill).all()
        for s in skills:
            graph.add_node(s.slug, skill_id=s.id, name=s.name)

        prereqs = self.db.query(SkillPrerequisite).all()
        for p in prereqs:
            target_skill = p.skill
            prereq_skill = p.prerequisite_skill
            if target_skill and prereq_skill:
                # Directed edge: prerequisite -> target
                graph.add_edge(
                    prereq_skill.slug,
                    target_skill.slug,
                    required_level=p.required_level
                )

        return graph

    def check_prerequisites_satisfied(
        self,
        skill_slug: str,
        current_skills: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Check if direct and recursive prerequisites for a given skill are satisfied by current learner skills.

        :param skill_slug: The skill being targeted
        :param current_skills: Dict mapping skill_slug to current proficiency level
        :return: Dict containing satisfaction boolean, readiness score (0.0-1.0), and missing prerequisites
        """
        if not self.dag.has_node(skill_slug):
            return {
                "is_satisfied": True,
                "readiness_score": 1.0,
                "missing_prerequisites": [],
                "direct_prerequisites": []
            }

        # Direct predecessors in DAG are prerequisites for skill_slug
        direct_prereqs = list(self.dag.predecessors(skill_slug))
        if not direct_prereqs:
            return {
                "is_satisfied": True,
                "readiness_score": 1.0,
                "missing_prerequisites": [],
                "direct_prerequisites": []
            }

        missing_prereqs = []
        total_prereqs = len(direct_prereqs)
        satisfied_count = 0

        for p_slug in direct_prereqs:
            edge_data = self.dag.get_edge_data(p_slug, skill_slug)
            req_lvl = edge_data.get("required_level", 1) if edge_data else 1
            curr_lvl = current_skills.get(p_slug, 0)

            if curr_lvl >= req_lvl:
                satisfied_count += 1
            else:
                p_node = self.dag.nodes[p_slug]
                missing_prereqs.append({
                    "skill_slug": p_slug,
                    "skill_name": p_node.get("name", p_slug),
                    "required_level": req_lvl,
                    "current_level": curr_lvl,
                    "gap": req_lvl - curr_lvl
                })

        is_satisfied = (len(missing_prereqs) == 0)
        readiness_score = satisfied_count / float(total_prereqs) if total_prereqs > 0 else 1.0

        return {
            "is_satisfied": is_satisfied,
            "readiness_score": round(readiness_score, 2),
            "missing_prerequisites": missing_prereqs,
            "direct_prerequisites": direct_prereqs
        }

    def get_prerequisite_chain(self, skill_slug: str) -> List[str]:
        """
        Get ancestor chain (all recursive prerequisites) in topological order for a target skill.
        """
        if not self.dag.has_node(skill_slug):
            return []

        ancestors = nx.ancestors(self.dag, skill_slug)
        if not ancestors:
            return []

        subgraph = self.dag.subgraph(ancestors.union({skill_slug}))
        topo_order = list(nx.topological_sort(subgraph))
        # Exclude target skill itself from returned prerequisites
        return [s for s in topo_order if s != skill_slug]

    def evaluate_resource_readiness(
        self,
        resource_target_skills: List[Tuple[str, int]],
        resource_prerequisite_skills: List[str],
        current_skills: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Evaluate readiness of a resource based on its target skills and declared prerequisite skills.

        :param resource_target_skills: List of (skill_slug, level_gained)
        :param resource_prerequisite_skills: List of prerequisite skill_slugs
        :param current_skills: Dict mapping skill_slug -> current_level
        :return: Dict containing overall satisfaction, readiness_score, missing_prereqs, status
        """
        all_prereq_slugs: Set[str] = set(resource_prerequisite_skills or [])

        # Also inspect DAG predecessors of primary target skills
        for s_slug, _ in resource_target_skills:
            if self.dag.has_node(s_slug):
                all_prereq_slugs.update(self.dag.predecessors(s_slug))

        if not all_prereq_slugs:
            return {
                "is_satisfied": True,
                "readiness_score": 1.0,
                "missing_prerequisites": [],
                "status": "ready"
            }

        missing = []
        satisfied_count = 0
        total_prereqs = len(all_prereq_slugs)

        for p_slug in sorted(all_prereq_slugs):
            curr_lvl = current_skills.get(p_slug, 0)
            # Find max required level from DAG or default 1
            req_lvl = 1
            for s_slug, _ in resource_target_skills:
                if self.dag.has_edge(p_slug, s_slug):
                    edge_data = self.dag.get_edge_data(p_slug, s_slug)
                    req_lvl = max(req_lvl, edge_data.get("required_level", 1))

            if curr_lvl >= req_lvl:
                satisfied_count += 1
            else:
                p_name = self.dag.nodes[p_slug].get("name", p_slug) if self.dag.has_node(p_slug) else p_slug
                missing.append({
                    "skill_slug": p_slug,
                    "skill_name": p_name,
                    "required_level": req_lvl,
                    "current_level": curr_lvl,
                    "gap": req_lvl - curr_lvl
                })

        readiness_score = satisfied_count / float(total_prereqs) if total_prereqs > 0 else 1.0
        is_satisfied = (len(missing) == 0)
        status = "ready" if is_satisfied else ("partially_ready" if readiness_score > 0 else "blocked")

        return {
            "is_satisfied": is_satisfied,
            "readiness_score": round(readiness_score, 2),
            "missing_prerequisites": missing,
            "status": status
        }
