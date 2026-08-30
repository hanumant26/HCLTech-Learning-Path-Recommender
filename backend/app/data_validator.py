"""
Comprehensive Data Validation Script for Learning Knowledge Base.
Enforces 12 strict integrity rules and NetworkX DAG validation.
"""
import sys
from pathlib import Path

# Ensure project root is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import networkx as nx
from backend.app.data.skills_data import SKILLS_DATA
from backend.app.data.careers_data import CAREERS_DATA, CAREER_SKILLS_DATA
from backend.app.data.prerequisites_data import PREREQUISITES_DATA
from backend.app.data.resources_data import RESOURCES_DATA
from backend.app.data.assessments_data import ASSESSMENTS_DATA

VALID_RESOURCE_TYPES = {"course", "project", "assessment", "practice", "tutorial"}
VALID_IMPORTANCE_LEVELS = {"critical", "high", "medium", "optional"}

def validate_knowledge_base() -> bool:
    """Validate knowledge base against 12 integrity rules."""
    errors = []
    warnings = []

    print("=== Starting Knowledge Base Data Validation ===")

    # 1. Duplicate skill IDs / slugs & 2. Duplicate skill names
    seen_skill_slugs = set()
    seen_skill_names = set()
    for idx, skill in enumerate(SKILLS_DATA):
        # 4. Missing required fields in skills
        for field in ["slug", "name", "category", "description"]:
            if not skill.get(field):
                errors.append(f"Rule 4 (Missing Field): Skill index {idx} missing field '{field}'.")

        slug = skill.get("slug")
        name = skill.get("name")

        if slug:
            if slug in seen_skill_slugs:
                errors.append(f"Rule 1 (Duplicate Skill Slug): '{slug}' found multiple times in SKILLS_DATA.")
            seen_skill_slugs.add(slug)

        if name:
            if name in seen_skill_names:
                errors.append(f"Rule 2 (Duplicate Skill Name): '{name}' found multiple times in SKILLS_DATA.")
            seen_skill_names.add(name)

    # 3. Duplicate resource IDs / slugs
    seen_resource_slugs = set()
    for idx, res in enumerate(RESOURCES_DATA):
        # 4. Missing required fields in resources
        for field in ["slug", "title", "provider", "resource_type", "duration_hours", "difficulty_level", "target_skills"]:
            if res.get(field) is None or res.get(field) == "":
                errors.append(f"Rule 4 (Missing Field): Resource index {idx} ('{res.get('slug')}') missing field '{field}'.")

        res_slug = res.get("slug")
        if res_slug:
            if res_slug in seen_resource_slugs:
                errors.append(f"Rule 3 (Duplicate Resource Slug): '{res_slug}' found multiple times in RESOURCES_DATA.")
            seen_resource_slugs.add(res_slug)

        # 10. Resources without target skills
        target_skills = res.get("target_skills", [])
        if not target_skills:
            errors.append(f"Rule 10 (Resource Without Target Skills): Resource '{res_slug}' has empty target_skills list.")

        # 11. Invalid resource types
        res_type = res.get("resource_type")
        if res_type and res_type not in VALID_RESOURCE_TYPES:
            errors.append(f"Rule 11 (Invalid Resource Type): Resource '{res_slug}' has invalid resource_type '{res_type}'. Allowed: {VALID_RESOURCE_TYPES}")

        # Validate resource target skills & prerequisites
        for s_slug, level, is_primary in target_skills:
            # 6. Invalid skill references
            if s_slug not in seen_skill_slugs:
                errors.append(f"Rule 6 (Invalid Skill Ref): Resource '{res_slug}' targets unknown skill '{s_slug}'.")
            # 9. Invalid proficiency levels
            if not (1 <= level <= 5):
                errors.append(f"Rule 9 (Invalid Proficiency): Resource '{res_slug}' target skill '{s_slug}' has invalid level {level} (must be 1-5).")

        for prereq_slug in res.get("prerequisites", []):
            if prereq_slug not in seen_skill_slugs:
                errors.append(f"Rule 7 (Invalid Prerequisite Ref): Resource '{res_slug}' references unknown prerequisite skill '{prereq_slug}'.")

    # 5. Invalid career references & career skill mappings validation
    seen_career_slugs = {c["slug"] for c in CAREERS_DATA}
    for cs in CAREER_SKILLS_DATA:
        c_slug = cs.get("career_slug")
        s_slug = cs.get("skill_slug")
        req_lvl = cs.get("required_level")
        importance = cs.get("importance")

        if c_slug not in seen_career_slugs:
            errors.append(f"Rule 5 (Invalid Career Ref): CareerSkill references unknown career '{c_slug}'.")
        if s_slug not in seen_skill_slugs:
            errors.append(f"Rule 6 (Invalid Skill Ref): CareerSkill for career '{c_slug}' references unknown skill '{s_slug}'.")
        if not (1 <= req_lvl <= 5):
            errors.append(f"Rule 9 (Invalid Proficiency): CareerSkill for '{c_slug}'/'{s_slug}' has invalid required_level {req_lvl}.")
        if importance not in VALID_IMPORTANCE_LEVELS:
            errors.append(f"Rule 4/5 (Invalid Importance): CareerSkill for '{c_slug}'/'{s_slug}' has invalid importance '{importance}'.")

    # 7. Invalid prerequisite references & 8. Circular prerequisite dependencies (DAG Check using NetworkX)
    dag = nx.DiGraph()
    for s_slug in seen_skill_slugs:
        dag.add_node(s_slug)

    for target_slug, prereq_slug, req_level in PREREQUISITES_DATA:
        if target_slug not in seen_skill_slugs:
            errors.append(f"Rule 7 (Invalid Prerequisite Target): Prerequisite target '{target_slug}' does not exist in SKILLS_DATA.")
        if prereq_slug not in seen_skill_slugs:
            errors.append(f"Rule 7 (Invalid Prerequisite Source): Prerequisite source '{prereq_slug}' does not exist in SKILLS_DATA.")
        if not (1 <= req_level <= 5):
            errors.append(f"Rule 9 (Invalid Prerequisite Level): Prerequisite ({target_slug} -> {prereq_slug}) has level {req_level}.")

        # Add directed edge from prereq_slug -> target_slug (prerequisite must come before target)
        if target_slug in seen_skill_slugs and prereq_slug in seen_skill_slugs:
            dag.add_edge(prereq_slug, target_slug)

    if not nx.is_directed_acyclic_graph(dag):
        cycles = list(nx.simple_cycles(dag))
        errors.append(f"Rule 8 (Circular Prerequisite Dependency): Prerequisite graph contains cycles: {cycles}")
    else:
        print("[OK] Prerequisite Graph validated as a Directed Acyclic Graph (DAG) using NetworkX.")

    # 12. Inconsistent skill names / slugs check in assessments
    for idx, asm in enumerate(ASSESSMENTS_DATA):
        s_slug = asm.get("skill_slug")
        if s_slug not in seen_skill_slugs:
            errors.append(f"Rule 12 (Inconsistent Skill Ref): Assessment '{asm.get('title')}' references unknown skill '{s_slug}'.")

        questions = asm.get("questions", [])
        if len(questions) < 4:
            errors.append(f"Rule 4 (Assessment Questions): Assessment '{asm.get('title')}' has fewer than 4 questions.")

        for q_idx, q in enumerate(questions):
            opts = q.get("options", [])
            ans = q.get("correct_answer")
            if ans not in opts:
                errors.append(f"Rule 4/12 (Assessment Answer Mismatch): Assessment '{asm.get('title')}' Q{q_idx+1} correct_answer '{ans}' is not in options {opts}.")

    # Summary report
    print(f"\nValidation Completed: {len(SKILLS_DATA)} Skills, {len(CAREERS_DATA)} Careers, {len(PREREQUISITES_DATA)} Prerequisites, {len(RESOURCES_DATA)} Resources, {len(ASSESSMENTS_DATA)} Assessments checked.")

    if errors:
        print(f"\n[ERROR] VALIDATION FAILED WITH {len(errors)} ERROR(S):")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("\n[SUCCESS] ALL 12 DATA VALIDATION RULES PASSED SUCCESSFULLY!")
        return True

if __name__ == "__main__":
    success = validate_knowledge_base()
    sys.exit(0 if success else 1)
