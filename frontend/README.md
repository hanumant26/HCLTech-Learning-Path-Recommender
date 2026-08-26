# AI-Powered Personalized Learning Path Recommender
## HCLTech AMPlified Round 2 Project

---

## 1. Project Overview & Architecture

The **AI-Powered Personalized Learning Path Recommender** is an intelligent assistant designed to solve choice paralysis in online education. It generates milestone-driven learning paths tailored to a learner's current skills, career goals, and available time budget.

### Hybrid Core Design
The platform uses a **Hybrid Architecture**:
- **Deterministic Core (NetworkX DAG + Python Scoring)**: Traverses skill prerequisites, calculates skill gaps, and ranks candidates using multi-factor mathematical scoring.
- **LLM Cognitive Layer (Gemini API)**: Parses natural language goal descriptions, extracts skills, and generates human-readable recommendation explanations.
- **Relational Data Foundation**: SQLAlchemy models for users, profiles, careers, skills, prerequisites, courses, paths, progress, and feedback.

```
Learner Goal
 → Learner Profile
 → Skill Gap Analysis
 → Prerequisite DAG
 → Candidate Resource Retrieval
 → Deterministic Recommendation Scoring
 → Personalized Learning Path
 → Progress & Feedback
 → Adaptive Path Repair
```

---

## 2. Project Foundation & Folder Structure

```
HCLTech-Learning-Path-Recommender/
├── README.md                          # Current setup and project architecture
├── requirements.txt                   # Backend dependencies (FastAPI, SQLAlchemy, NetworkX, Pytest)
├── backend/
│   ├── seed_data.py                   # Top-level seed script execution entrypoint
│   ├── app/
│   │   ├── main.py                    # FastAPI app entrypoint with health check & DB startup
│   │   ├── seed_data.py               # Foundational seeding mechanism (5 careers, skills, prereqs)
│   │   ├── api/                       # API router definitions
│   │   ├── core/                      # Core configuration and database session management
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/                    # SQLAlchemy database models (15 relational tables)
│   │   │   ├── user.py
│   │   │   ├── profile.py
│   │   │   ├── skill.py
│   │   │   ├── career.py
│   │   │   ├── course.py
│   │   │   ├── learning_path.py
│   │   │   ├── progress.py
│   │   │   ├── feedback.py
│   │   │   └── assessment.py
│   │   ├── schemas/                   # Pydantic schemas (V2 validation models)
│   │   ├── services/                  # Business & recommendation logic modules
│   │   └── tests/                     # Database and schema unit tests
│   └── data/
│       ├── README.md                  # Data quality & curation guidelines
│       └── data_dictionary.md         # Full schema reference dictionary
```

---

## 3. Database Schema

The database model contains 15 relational tables defined in SQLAlchemy with foreign keys, indexes, timestamps, and check constraints:

1. `users`: User identity & activity status.
2. `learner_profiles`: Learner target role, weekly hours, experience level, preferences.
3. `skills`: Canonical skill catalog (Programming Languages, Frameworks, Concepts, Tools).
4. `user_skills`: Learner current proficiency levels (1–5).
5. `careers`: Supported career goals (Data Scientist, AI Engineer, ML Engineer, Data Analyst, Full Stack Dev).
6. `career_skills`: Career skill requirements (1–5) and core indicators.
7. `skill_prerequisites`: Directed Graph prerequisite dependencies between skills.
8. `courses`: Learning resources (courses, projects, tutorials) with difficulty and ratings.
9. `course_skills`: Skill level gains provided by courses.
10. `learning_paths`: Generated learning roadmap containers.
11. `path_items`: Sequential items (milestones, courses, projects) within a path.
12. `progress`: Completion percentage (0–100%) and time spent.
13. `feedback`: Learner ratings (`too_easy`, `appropriate`, `too_difficult`, `not_relevant`).
14. `assessments`: Milestone quizzes and skill checks.
15. `assessment_results`: Learner test scores and pass/fail attempts.

---

## 4. How to Run the Backend Locally

### Prerequisites
- Python 3.11+ installed

### Step 1: Virtual Environment Setup & Dependencies
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Initialize Database & Seed Foundational Data
```powershell
python backend/seed_data.py
```

### Step 3: Run Unit Tests
```powershell
.\venv\Scripts\python.exe -m pytest
```

### Step 4: Start Development Server (Manual)
```powershell
uvicorn backend.app.main:app --reload
```
- Interactive Swagger API docs available at: `http://127.0.0.1:8000/docs`
- Health check endpoint: `http://127.0.0.1:8000/health`
