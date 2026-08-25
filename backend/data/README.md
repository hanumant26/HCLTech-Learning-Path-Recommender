# Knowledge Base & Learning Resource Curation Guidelines

## Overview
This directory contains the curated Knowledge Base for the AI-Powered Personalized Learning Path Recommender system. It includes the canonical technical skills taxonomy, career requirements, Directed Acyclic Graph (DAG) skill prerequisite relationships, learning resources catalog, practical projects, and diagnostic assessments.

## Data Quality Principles & Curation Strategy
1. **Verified Real Resources**: All courses, books, tutorials, and documentation links reference verified real-world platforms (Coursera, Udemy, fast.ai, MIT OpenCourseWare, freeCodeCamp, Kaggle, MDN Web Docs, PyTorch, Hugging Face, Scikit-Learn).
2. **No Fake Data Guarantee**:
   - If a verified URL is unavailable, `url` is left as an empty string `""` / `None`.
   - If a rating is unverified, `rating` is set to `None` / `null`. Fake or randomly generated ratings are strictly prohibited.
3. **Canonical Skill Taxonomy**: Standardized skill slugs and names prevent fragmentation (e.g., single canonical name `"Machine Learning"` instead of split terms like `"ML"` or `"Machine-Learning"`).
4. **DAG Prerequisite Integrity**: Prerequisites form a Directed Acyclic Graph (DAG) enforced via NetworkX. Cyclical dependencies and self-referential loops are strictly forbidden.
5. **Idempotent Seeding**: Seeding mechanisms insert or update records cleanly without introducing duplicates upon re-execution.

## File Map
- `data_dictionary.md`: Full relational schema reference for all 15 database tables.
- `knowledge_base_summary.md`: Quantitative statistics summary for skills, careers, prerequisites, resources, projects, and assessments.
- `validate_knowledge_base.py` / `data_validator.py`: Automated validation script enforcing 12 integrity rules.
