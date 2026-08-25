"""
Recommendation Engine Demo Script.
Runs 4 realistic scenarios to demonstrate the core recommendation engine and personalized learning path generator.
"""
import sys
import json
from pathlib import Path

# Ensure project root is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.core.database import SessionLocal, init_db
from backend.app.seed_data import seed_foundational_data
from backend.app.services.recommendation_engine import RecommendationEngine


def print_section_header(title: str):
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)


def run_scenario(engine: RecommendationEngine, db, scenario_num: int, name: str, profile: dict):
    print_section_header(f"SCENARIO {scenario_num}: {name}")
    print(f"Target Career: {profile.get('target_career')}")
    print(f"Weekly Hours:  {profile.get('weekly_hours')}")
    print(f"Learner Skills: {json.dumps(profile.get('skills'), indent=2)}")

    result = engine.generate_recommendations(profile_data=profile, db=db, top_n=5)

    print("\n--- SKILL GAP REPORT ---")
    summary = result["skill_gap_report"]["summary"]
    print(f"Overall Readiness: {summary['readiness_percentage']}%")
    print(f"Skills Summary: {summary['proficient_count']} Proficient | {summary['minor_gap_count']} Minor Gap | {summary['critical_gap_count']} Critical Gap")

    print("\nDetailed Skill Gaps:")
    for g in result["skill_gap_report"]["skill_gaps"]:
        status_flag = "[CRITICAL]" if g["status"] == "critical" else ("[MINOR]" if g["status"] == "minor" else "[PROFICIENT]")
        print(f"  - {g['skill']} (Req: L{g['required_level']}, Curr: L{g['current_level']}, Gap: {g['gap']}) {status_flag}")

    print("\n--- TOP RECOMMENDED RESOURCES ---")
    for idx, rec in enumerate(result["recommendations"], 1):
        print(f"\n{idx}. [{rec['score']}/100] {rec['title']} ({rec['provider']})")
        print(f"   Type: {rec['resource_type']} | Difficulty: {rec['difficulty_level']} | Duration: {rec['duration_hours']} hrs | Rating: {rec['rating']}")
        print(f"   Readiness: {rec['readiness_status']} | Reasons: {', '.join(rec['reason_codes'])}")
        print(f"   Breakdown: {rec['breakdown']}")
        if rec.get("missing_prerequisites"):
            print(f"   Missing Prereqs: {[m['skill_name'] for m in rec['missing_prerequisites']]}")

    print("\n--- PERSONALIZED ROADMAP ---")
    roadmap = result["learning_path"]
    print(f"Total Hours: {roadmap['total_estimated_hours']} hrs | Estimated Duration: {roadmap['total_estimated_weeks']} weeks @ {roadmap['weekly_hours']} hrs/week")

    for phase in roadmap["phases"]:
        print(f"\n[{phase['phase_name']}] ({phase['phase_hours']} hrs)")
        for item in phase["items"]:
            print(f"  Step {item['sequence_order']}: [{item['item_type'].upper()}] {item['title']} ({item['estimated_hours']} hrs) - Status: {item['readiness_status']}")

    return result


def main():
    print("Initializing Database & Seeding Knowledge Base...")
    init_db()
    db = SessionLocal()

    try:
        # Seed DB idempotently to ensure full catalog is present
        seed_foundational_data(db)

        engine = RecommendationEngine()

        # SCENARIO 1: Data Scientist Learner with foundational gaps
        scenario_1 = {
            "target_career": "Data Scientist",
            "weekly_hours": 8,
            "skills": {
                "Python": 3,
                "SQL": 2,
                "Statistics": 1,
                "Pandas": 0,
                "Machine Learning": 0
            },
            "completed_resources": []
        }
        run_scenario(engine, db, 1, "Data Scientist (Beginner/Intermediate with Gaps)", scenario_1)

        # SCENARIO 2: AI Engineer Learner skipping beginner python
        scenario_2 = {
            "target_career": "AI Engineer",
            "weekly_hours": 12,
            "skills": {
                "Python": 4,
                "Machine Learning": 3,
                "Deep Learning": 1
            },
            "completed_resources": []
        }
        run_scenario(engine, db, 2, "AI Engineer (Advanced ML Learner)", scenario_2)

        # SCENARIO 3: Full Stack Developer focusing on React & Node.js
        scenario_3 = {
            "target_career": "Full Stack Developer",
            "weekly_hours": 10,
            "skills": {
                "HTML/CSS": 4,
                "JavaScript": 3,
                "React": 0,
                "Node.js": 0
            },
            "completed_resources": []
        }
        run_scenario(engine, db, 3, "Full Stack Developer (Frontend to Fullstack)", scenario_3)

        # SCENARIO 4: Expert Learner with high proficiencies
        scenario_4 = {
            "target_career": "Data Scientist",
            "weekly_hours": 15,
            "skills": {
                "Python": 5,
                "SQL": 4,
                "Statistics": 4,
                "Pandas": 5,
                "Machine Learning": 4,
                "Deep Learning": 4
            },
            "completed_resources": []
        }
        run_scenario(engine, db, 4, "Expert Learner (Near Complete Proficiency)", scenario_4)

        print_section_header("DEMO EXECUTED SUCCESSFULLY")

    finally:
        db.close()


if __name__ == "__main__":
    main()
