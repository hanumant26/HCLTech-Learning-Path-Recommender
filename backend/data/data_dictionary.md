# Data Dictionary: AI-Powered Personalized Learning Path Recommender

---

## 1. `users`
Stores user identities and account status.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `email` (VARCHAR(255), Unique, Indexed, NOT NULL)
- `name` (VARCHAR(255), NOT NULL)
- `is_active` (BOOLEAN, Default: `True`, NOT NULL)
- `created_at` (DATETIME, Default: `UTC now`, NOT NULL)
- `updated_at` (DATETIME, Default: `UTC now`, NOT NULL)

---

## 2. `learner_profiles`
Captures learner background, target goal, time commitment, and preferences.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `user_id` (INTEGER, Foreign Key -> `users.id` ON DELETE CASCADE, Unique, Indexed, NOT NULL)
- `target_role` (VARCHAR(100), Indexed, NULLABLE)
- `weekly_hours` (INTEGER, Default: `10`, NOT NULL)
- `experience_level` (VARCHAR(50), Default: `'beginner'`, NOT NULL)
- `preferred_learning_style` (VARCHAR(50), Default: `'mixed'`, NOT NULL)
- `created_at` (DATETIME, NOT NULL)
- `updated_at` (DATETIME, NOT NULL)

---

## 3. `skills`
Master catalog of 95 canonical skills across 15 technical domains.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `slug` (VARCHAR(50), Unique, Indexed, NOT NULL)
- `name` (VARCHAR(100), Unique, NOT NULL)
- `category` (VARCHAR(50), Indexed, NOT NULL) -- Programming Language, Data Science, Statistics, Mathematics, Machine Learning, Deep Learning, NLP, Computer Vision, Databases, Web Development, Backend Development, Frontend Development, Software Engineering, Tools & Version Control, DevOps & Cloud Basics, Analytics & BI
- `description` (TEXT, NULLABLE)
- `created_at` (DATETIME, NOT NULL)
- `updated_at` (DATETIME, NOT NULL)

---

## 4. `user_skills`
Junction table tracking current user proficiency levels (1–5).
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `profile_id` (INTEGER, Foreign Key -> `learner_profiles.id` ON DELETE CASCADE, Indexed, NOT NULL)
- `skill_id` (INTEGER, Foreign Key -> `skills.id` ON DELETE CASCADE, Indexed, NOT NULL)
- `proficiency_level` (INTEGER, NOT NULL)
- `created_at` (DATETIME, NOT NULL)
- `updated_at` (DATETIME, NOT NULL)
- **Constraints**: 
  - `CHECK (proficiency_level >= 1 AND proficiency_level <= 5)`
  - `UNIQUE (profile_id, skill_id)`

---

## 5. `careers`
Catalog of 5 supported career goal trajectories.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `slug` (VARCHAR(50), Unique, Indexed, NOT NULL)
- `title` (VARCHAR(100), Unique, NOT NULL) -- Data Scientist, AI Engineer, Machine Learning Engineer, Data Analyst, Full Stack Developer
- `description` (TEXT, NULLABLE)
- `created_at` (DATETIME, NOT NULL)
- `updated_at` (DATETIME, NOT NULL)

---

## 6. `career_skills`
Defines required skill proficiencies and importance for target career roles.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `career_id` (INTEGER, Foreign Key -> `careers.id` ON DELETE CASCADE, Indexed, NOT NULL)
- `skill_id` (INTEGER, Foreign Key -> `skills.id` ON DELETE CASCADE, Indexed, NOT NULL)
- `required_level` (INTEGER, NOT NULL) -- (1–5)
- `importance` (VARCHAR(20), Default: `'high'`, NOT NULL) -- `critical`, `high`, `medium`, `optional`
- `is_core` (BOOLEAN, Default: `True`, NOT NULL)
- `created_at` (DATETIME, NOT NULL)
- `updated_at` (DATETIME, NOT NULL)
- **Constraints**:
  - `CHECK (required_level >= 1 AND required_level <= 5)`
  - `UNIQUE (career_id, skill_id)`

---

## 7. `skill_prerequisites`
Directed Acyclic Graph (DAG) relationship defining prerequisites between skills.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `skill_id` (INTEGER, Foreign Key -> `skills.id` ON DELETE CASCADE, Indexed, NOT NULL) -- Target skill requiring prerequisite
- `prerequisite_skill_id` (INTEGER, Foreign Key -> `skills.id` ON DELETE CASCADE, Indexed, NOT NULL) -- Prerequisite skill needed
- `required_level` (INTEGER, Default: `1`, NOT NULL) -- (1–5)
- `created_at` (DATETIME, NOT NULL)
- `updated_at` (DATETIME, NOT NULL)
- **Constraints**:
  - `CHECK (required_level >= 1 AND required_level <= 5)`
  - `CHECK (skill_id != prerequisite_skill_id)`
  - `UNIQUE (skill_id, prerequisite_skill_id)`

---

## 8. `courses`
Catalog of learning resources (courses, projects, practice, tutorials, assessments).
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `slug` (VARCHAR(100), Unique, Indexed, NOT NULL)
- `title` (VARCHAR(200), NOT NULL)
- `description` (TEXT, NULLABLE)
- `provider` (VARCHAR(100), Indexed, NOT NULL)
- `url` (VARCHAR(500), NULLABLE) -- Empty if unavailable, no fake URLs
- `resource_type` (VARCHAR(50), Default: `'course'`, NOT NULL) -- `course`, `project`, `assessment`, `practice`, `tutorial`
- `learning_format` (VARCHAR(50), Default: `'interactive'`, NOT NULL) -- `video`, `text`, `interactive`, `project`
- `is_project_based` (BOOLEAN, Default: `False`, NOT NULL)
- `duration_hours` (FLOAT, NOT NULL)
- `difficulty_level` (VARCHAR(20), Default: `'intermediate'`, NOT NULL) -- `beginner`, `intermediate`, `advanced`
- `rating` (FLOAT, NULLABLE) -- Null if unverified, no fake ratings
- `created_at` (DATETIME, NOT NULL)
- `updated_at` (DATETIME, NOT NULL)
- **Constraints**:
  - `CHECK (rating IS NULL OR (rating >= 0.0 AND rating <= 5.0))`

---

## 9. `course_skills`
Skill outcome mapping for learning resources.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `course_id` (INTEGER, Foreign Key -> `courses.id` ON DELETE CASCADE, Indexed, NOT NULL)
- `skill_id` (INTEGER, Foreign Key -> `skills.id` ON DELETE CASCADE, Indexed, NOT NULL)
- `level_gained` (INTEGER, Default: `1`, NOT NULL) -- (1–5)
- `is_primary` (BOOLEAN, Default: `True`, NOT NULL)
- `created_at` (DATETIME, NOT NULL)
- `updated_at` (DATETIME, NOT NULL)
- **Constraints**:
  - `CHECK (level_gained >= 1 AND level_gained <= 5)`
  - `UNIQUE (course_id, skill_id)`

---

## 10. `learning_paths`
Container for generated personalized learning roadmaps.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `profile_id` (INTEGER, Foreign Key -> `learner_profiles.id` ON DELETE CASCADE, Indexed, NOT NULL)
- `career_id` (INTEGER, Foreign Key -> `careers.id` ON DELETE SET NULL, Indexed, NULLABLE)
- `title` (VARCHAR(200), NOT NULL)
- `status` (VARCHAR(50), Default: `'active'`, NOT NULL)
- `total_estimated_hours` (FLOAT, Default: `0.0`, NOT NULL)
- `created_at` (DATETIME, NOT NULL)
- `updated_at` (DATETIME, NOT NULL)

---

## 11. `path_items`
Sequential items (milestones, courses, projects) in a learning path.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `path_id` (INTEGER, Foreign Key -> `learning_paths.id` ON DELETE CASCADE, Indexed, NOT NULL)
- `course_id` (INTEGER, Foreign Key -> `courses.id` ON DELETE SET NULL, Indexed, NULLABLE)
- `item_type` (VARCHAR(50), Default: `'course'`, NOT NULL)
- `title` (VARCHAR(200), NOT NULL)
- `phase_number` (INTEGER, Default: `1`, NOT NULL)
- `sequence_order` (INTEGER, Default: `1`, NOT NULL)
- `status` (VARCHAR(50), Default: `'not_started'`, NOT NULL)
- `is_prerequisite_satisfied` (BOOLEAN, Default: `True`, NOT NULL)
- `created_at` (DATETIME, NOT NULL)
- `updated_at` (DATETIME, NOT NULL)

---

## 12. `progress`
Fine-grained completion metrics for each path item.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `path_item_id` (INTEGER, Foreign Key -> `path_items.id` ON DELETE CASCADE, Unique, Indexed, NOT NULL)
- `completion_pct` (FLOAT, Default: `0.0`, NOT NULL)
- `time_spent_mins` (INTEGER, Default: `0`, NOT NULL)
- `completed_at` (DATETIME, NULLABLE)
- `created_at` (DATETIME, NOT NULL)
- `updated_at` (DATETIME, NOT NULL)
- **Constraints**:
  - `CHECK (completion_pct >= 0.0 AND completion_pct <= 100.0)`

---

## 13. `feedback`
Learner feedback on path items to trigger dynamic path adaptation.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `path_item_id` (INTEGER, Foreign Key -> `path_items.id` ON DELETE CASCADE, Indexed, NOT NULL)
- `user_id` (INTEGER, Foreign Key -> `users.id` ON DELETE CASCADE, Indexed, NOT NULL)
- `rating_type` (VARCHAR(50), NOT NULL) -- `too_easy`, `appropriate`, `too_difficult`, `not_relevant`
- `comment` (TEXT, NULLABLE)
- `created_at` (DATETIME, NOT NULL)

---

## 14. `assessments`
Milestone quizzes and diagnostic skill evaluations.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `path_item_id` (INTEGER, Foreign Key -> `path_items.id` ON DELETE CASCADE, Indexed, NULLABLE)
- `skill_id` (INTEGER, Foreign Key -> `skills.id` ON DELETE CASCADE, Indexed, NULLABLE)
- `title` (VARCHAR(200), NOT NULL)
- `description` (VARCHAR(500), NULLABLE)
- `passing_score_pct` (FLOAT, Default: `70.0`, NOT NULL)
- `questions` (JSON, NULLABLE) -- Array of 5 diagnostic MCQs with question, options, correct_answer, difficulty, skill_tested
- `created_at` (DATETIME, NOT NULL)
- `updated_at` (DATETIME, NOT NULL)

---

## 15. `assessment_results`
Learner score records on assessments.
- `id` (INTEGER, Primary Key, Auto-increment, Indexed)
- `assessment_id` (INTEGER, Foreign Key -> `assessments.id` ON DELETE CASCADE, Indexed, NOT NULL)
- `user_id` (INTEGER, Foreign Key -> `users.id` ON DELETE CASCADE, Indexed, NOT NULL)
- `score_pct` (FLOAT, NOT NULL)
- `passed` (BOOLEAN, NOT NULL)
- `attempt_number` (INTEGER, Default: `1`, NOT NULL)
- `created_at` (DATETIME, NOT NULL)
