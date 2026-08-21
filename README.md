# AI-Powered Personalized Learning Path Recommender
## HCLTech AMPlified Round 2 Project

---

## 1. Project Overview & Architecture

The **AI-Powered Personalized Learning Path Recommender** is an intelligent assistant designed to solve choice paralysis in online education. It generates milestone-driven learning paths tailored to a learner's current skills, career goals, and available time budget.

### Hybrid Core Design
The platform uses a **Hybrid Architecture**:
- **Deterministic Core (NetworkX DAG + Python Scoring)**: Traverses skill prerequisites, calculates skill gaps, and ranks candidates using multi-factor mathematical scoring.
- **LLM Cognitive Layer (Gemini API + Grounded Fallback Engine)**: Provides conversational explanations, answers roadmap questions, and generates human-readable reasoning strictly grounded in deterministic backend outputs.
- **FastAPI API Layer**: Exposes clean, typed REST endpoints connecting the backend intelligence with the user interface.
- **Relational Data Foundation**: SQLAlchemy models for users, profiles, careers, skills, prerequisites, courses, paths, progress, and feedback.

```
Learner Goal & Profile
 → Skill Gap Analysis
 → Prerequisite DAG Traversal
 → Candidate Resource Retrieval
 → Deterministic Recommendation Scoring
 → Personalized Learning Path Generation
 → FastAPI REST Endpoints
 → Conversational LLM Assistant (Grounded Explanations)
 → Progress & Feedback Tracking
 → Adaptive Path Repair
```

---

## 2. Project Foundation & Folder Structure

```
HCLTech-Learning-Path-Recommender/
├── README.md                          # Current setup, architecture, and project documentation
├── requirements.txt                   # Backend dependencies (FastAPI, SQLAlchemy, NetworkX, Pytest, Pydantic)
├── learning_recommender.db            # SQLite database instance
├── backend/
│   ├── seed_data.py                   # Top-level seed script execution entrypoint
│   ├── data_validator.py              # Knowledge base data integrity validator
│   ├── demo_recommendation.py         # Standalone CLI recommendation demo script
│   ├── app/
│   │   ├── main.py                    # FastAPI app entrypoint, CORS, routers & health check
│   │   ├── seed_data.py               # Foundational seeding mechanism (5 careers, 95 skills, 84 prereqs)
│   │   ├── api/                       # API router definitions
│   │   │   ├── __init__.py
│   │   │   ├── careers.py             # GET /api/careers
│   │   │   ├── skills.py              # GET /api/skills
│   │   │   ├── learner.py             # POST /api/learner/profile
│   │   │   ├── recommendations.py     # POST /api/recommendations/generate
│   │   │   ├── learning_path.py       # POST /api/learning-path
│   │   │   └── assistant.py           # POST /api/assistant/chat, explain-resource, GET /api/assistant/status
│   │   ├── core/                      # Core configuration and database session management
│   │   │   ├── config.py              # Application settings, LLM settings & environment configuration
│   │   │   └── database.py            # SQLAlchemy engine, SessionLocal, and init_db
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
│   │   │   ├── api_responses.py       # Unified API response models
│   │   │   ├── assistant.py           # Phase 5 assistant request/response schemas
│   │   │   ├── career.py
│   │   │   ├── course.py
│   │   │   ├── feedback.py
│   │   │   ├── learning_path.py
│   │   │   ├── profile.py
│   │   │   ├── progress.py
│   │   │   ├── skill.py
│   │   │   └── user.py
│   │   ├── services/                  # Business & recommendation logic modules
│   │   │   ├── assistant_service.py   # Grounded LLM and deterministic fallback assistant service
│   │   │   ├── candidate_retriever.py # Resource candidate retrieval by skill gap
│   │   │   ├── exceptions.py          # Domain-specific exception definitions
│   │   │   ├── learning_path_generator.py # Milestone and sequential roadmap generator
│   │   │   ├── prerequisite_engine.py # NetworkX DAG prerequisite resolution & unlock checks
│   │   │   ├── recommendation_engine.py # Multi-factor recommendation engine
│   │   │   ├── scoring.py             # Multi-factor mathematical scoring algorithms
│   │   │   ├── skill_gap.py           # Skill gap analyzer comparing profile vs career requirements
│   │   │   └── skill_normalizer.py    # Canonical skill resolution and alias mapping
│   │   └── tests/                     # Database and schema unit tests
│   │       ├── test_database.py
│   │       └── test_knowledge_base.py
│   ├── data/
│   │   ├── README.md                  # Data quality & curation guidelines
│   │   ├── data_dictionary.md         # Full schema reference dictionary
│   │   └── knowledge_base_summary.md  # Knowledge base catalog statistics
│   └── tests/                         # Comprehensive unit & API integration test suite
│       ├── conftest.py                # Pytest fixtures and test database setup
│       ├── test_api_assistant.py      # Phase 5 assistant endpoint tests
│       ├── test_api_careers.py        # Phase 4 careers endpoint tests
│       ├── test_api_learner.py        # Phase 4 learner profile endpoint tests
│       ├── test_api_learning_path.py  # Phase 4 learning path endpoint tests
│       ├── test_api_recommendations.py# Phase 4 recommendation endpoint tests
│       ├── test_api_skills.py         # Phase 4 skills endpoint tests
│       ├── test_assistant_service.py  # Phase 5 assistant service logic tests
│       ├── test_candidate_retrieval.py# Candidate retriever unit tests
│       ├── test_learning_path.py      # Learning path generator unit tests
│       ├── test_prerequisite_engine.py# Prerequisite engine & DAG unit tests
│       ├── test_recommendation_engine.py # Recommendation engine unit tests
│       ├── test_scoring.py            # Scoring formula unit tests
│       └── test_skill_gap.py          # Skill gap calculation unit tests
```

---

## 3. Database Schema

The database model contains 15 relational tables defined in SQLAlchemy with foreign keys, indexes, timestamps, and check constraints:

1. `users`: User identity and activity status.
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

## 4. Phase 4: FastAPI REST API Layer

Phase 4 exposes the deterministic recommendation engine and profile management via RESTful endpoints mounted under the `/api` prefix:

### Implemented Endpoints

1. **`GET /api/careers`**
   - Retrieves all supported career paths with required target skills, proficiency expectations, and role descriptions.
2. **`GET /api/skills`**
   - Returns the canonical skill catalog categorized across domains with proficiency level descriptions (1 to 5).
3. **`POST /api/learner/profile`**
   - Creates or updates a learner profile, storing target career, weekly time commitment, and existing skill proficiencies.
4. **`POST /api/recommendations/generate`**
   - Computes skill gaps, checks prerequisite DAG readiness, and returns scored, ranked learning resource recommendations.
5. **`POST /api/learning-path`**
   - Generates and persists a structured, sequential, milestone-based learning roadmap tailored to the learner's schedule.

---

## 5. Phase 5: LLM Conversational Assistant

Phase 5 introduces a conversational AI assistant that provides grounded, personalized guidance and explains recommendations, locks, and roadmaps without hallucinations.

### Implemented Endpoints

1. **`POST /api/assistant/chat`**
   - Interactive conversational endpoint supporting dynamic learner queries grounded in profile, skill gap, and recommendation context.
2. **`POST /api/assistant/explain-resource`**
   - Generates focused explanations for why a specific course/resource card was recommended or why it is locked by prerequisites.
3. **`GET /api/assistant/status`**
   - Reports assistant engine health, active provider (`gemini` or `deterministic-fallback`), and model configuration.

### Supported Question Types

1. **Why Recommended**: Explains the exact scoring rationale, skill target coverage, and match quality for a recommended course.
2. **Why Locked**: Identifies missing prerequisite skills blocking a course and outlines the prerequisite sequence required to unlock it.
3. **What to Learn Next**: Pinpoints immediate next steps based on Phase 1 milestone readiness and weekly time availability.
4. **Skip Prerequisite**: Assesses risks of skipping foundational courses, highlighting knowledge dependencies and offering structured advice.
5. **Limited Weekly Time**: Provides customized pacing strategies, milestone timelines, and high-priority focus areas for constrained time budgets.

### Phase 5 Evaluation & Verification

- **Automated Tests**: 102/102 passed across database, engine, API routers, and assistant service test suites.
- **Manual Tests**: 5/5 passed across all supported conversational question scenarios.
- **Fallback Engine Verified**: Automatically falls back to a deterministic rule-based conversational engine when `GEMINI_API_KEY` is not present or unreachable.
- **Grounded Responses Verified**: Responses strictly reference verified profile data, DAG prerequisites, and recommendation scores with zero hallucination.
- **HTTP 200 Verified**: All endpoints return standard HTTP 200 responses with validated Pydantic schemas.

---

## 6. Project Progress & Implementation Status

| Phase / Component | Description | Status |
|---|---|---|
| **Phase 1: Database Architecture & Schema** | 15 SQLAlchemy relational models, constraints, and relationships | Completed |
| **Phase 2: Curated Knowledge Base** | 5 careers, 95 skills, 84 prerequisite links, 171 resources | Completed |
| **Phase 3: Recommendation Engine** | Skill gap analysis, NetworkX DAG traversal, multi-factor scoring | Completed |
| **Phase 4: FastAPI REST API Layer** | 5 core endpoints for careers, skills, profile, recommendations, path | Completed |
| **Phase 5: LLM Conversational Assistant** | Grounded Q&A assistant, 5 intent handlers, fallback engine | Completed |
| **Phase 6: Progress & Feedback Loop** | Course completion tracking, ratings, and adaptive path repair | In Progress / Pending |
| **Phase 7: Frontend Web Application** | Interactive React / Tailwind dashboard and conversational UI | In Progress / Pending |
| **Phase 8: End-to-End Integration Testing** | Frontend-to-backend end-to-end integration test flows | Pending |
| **Phase 9: Deployment & Final Documentation** | Production containerization, deployment configs, and demo docs | Pending |

---

## 7. How to Run the Backend Locally

### Prerequisites
- Python 3.11+ installed

### Step 1: Virtual Environment Setup & Dependencies
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Environment Configuration (Optional for LLM)
Create a `.env` file in the project root if you want to use the live Gemini LLM engine (otherwise the deterministic fallback engine will be used automatically):
```env
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL=gemini-1.5-flash
LLM_TEMPERATURE=0.2
```

### Step 3: Initialize Database & Seed Foundational Data
```powershell
python backend/seed_data.py
```

### Step 4: Run Unit & API Test Suite
```powershell
.\venv\Scripts\python.exe -m pytest
```

### Step 5: Start Development Server
```powershell
uvicorn backend.app.main:app --reload
```
- Interactive Swagger API docs: `http://127.0.0.1:8000/docs`
- Health check endpoint: `http://127.0.0.1:8000/health`
- Assistant status endpoint: `http://127.0.0.1:8000/api/assistant/status`
