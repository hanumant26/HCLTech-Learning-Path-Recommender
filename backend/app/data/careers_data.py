"""
Career Definitions and Career-to-Skill Requirements Mappings for 5 Target Careers.
"""

CAREERS_DATA = [
    {
        "slug": "data-scientist",
        "title": "Data Scientist",
        "description": "Analyzes complex datasets to extract insights, build predictive models, and drive data-driven decision making."
    },
    {
        "slug": "ai-engineer",
        "title": "AI Engineer",
        "description": "Designs and deploys artificial intelligence systems, LLM applications, deep neural networks, and agentic workflows."
    },
    {
        "slug": "machine-learning-engineer",
        "title": "Machine Learning Engineer",
        "description": "Develops production machine learning pipelines, trains models, and optimizes model inference and deployment."
    },
    {
        "slug": "data-analyst",
        "title": "Data Analyst",
        "description": "Transforms raw data into actionable insights through SQL queries, visualization dashboards, and business intelligence."
    },
    {
        "slug": "full-stack-developer",
        "title": "Full Stack Developer",
        "description": "Builds end-to-end web applications covering responsive frontends, backend APIs, and database architectures."
    }
]

CAREER_SKILLS_DATA = [
    # 1. Data Scientist Requirements
    {"career_slug": "data-scientist", "skill_slug": "python", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "sql", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "pandas", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "numpy", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "exploratory-data-analysis", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "descriptive-statistics", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "inferential-statistics", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "hypothesis-testing", "required_level": 4, "importance": "high", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "probability-theory", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "linear-algebra", "required_level": 3, "importance": "medium", "is_core": False},
    {"career_slug": "data-scientist", "skill_slug": "machine-learning-fundamentals", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "supervised-learning", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "unsupervised-learning", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "scikit-learn", "required_level": 4, "importance": "high", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "feature-engineering", "required_level": 4, "importance": "high", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "xgboost-lightgbm", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "matplotlib-seaborn", "required_level": 4, "importance": "high", "is_core": True},
    {"career_slug": "data-scientist", "skill_slug": "git-github", "required_level": 3, "importance": "medium", "is_core": False},

    # 2. AI Engineer Requirements
    {"career_slug": "ai-engineer", "skill_slug": "python", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "linear-algebra", "required_level": 3, "importance": "medium", "is_core": False},
    {"career_slug": "ai-engineer", "skill_slug": "multivariable-calculus", "required_level": 3, "importance": "medium", "is_core": False},
    {"career_slug": "ai-engineer", "skill_slug": "deep-learning-fundamentals", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "neural-networks", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "pytorch", "required_level": 4, "importance": "high", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "transformers", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "nlp-fundamentals", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "large-language-models", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "prompt-engineering", "required_level": 4, "importance": "high", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "retrieval-augmented-generation", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "langchain", "required_level": 4, "importance": "high", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "fastapi", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "model-deployment", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "docker", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "ai-engineer", "skill_slug": "git-github", "required_level": 3, "importance": "high", "is_core": True},

    # 3. Machine Learning Engineer Requirements
    {"career_slug": "machine-learning-engineer", "skill_slug": "python", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "sql", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "linear-algebra", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "machine-learning-fundamentals", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "supervised-learning", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "scikit-learn", "required_level": 4, "importance": "high", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "deep-learning-fundamentals", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "pytorch", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "feature-engineering", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "model-evaluation", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "model-deployment", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "fastapi", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "docker", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "machine-learning-engineer", "skill_slug": "ci-cd", "required_level": 3, "importance": "medium", "is_core": False},
    {"career_slug": "machine-learning-engineer", "skill_slug": "git-github", "required_level": 4, "importance": "high", "is_core": True},

    # 4. Data Analyst Requirements
    {"career_slug": "data-analyst", "skill_slug": "sql", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-analyst", "skill_slug": "excel-advanced", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-analyst", "skill_slug": "python", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "data-analyst", "skill_slug": "pandas", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "data-analyst", "skill_slug": "descriptive-statistics", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-analyst", "skill_slug": "exploratory-data-analysis", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-analyst", "skill_slug": "data-visualization", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "data-analyst", "skill_slug": "power-bi", "required_level": 4, "importance": "high", "is_core": True},
    {"career_slug": "data-analyst", "skill_slug": "tableau", "required_level": 3, "importance": "medium", "is_core": False},
    {"career_slug": "data-analyst", "skill_slug": "relational-databases", "required_level": 3, "importance": "high", "is_core": True},

    # 5. Full Stack Developer Requirements
    {"career_slug": "full-stack-developer", "skill_slug": "html-css", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "full-stack-developer", "skill_slug": "javascript", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "full-stack-developer", "skill_slug": "typescript", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "full-stack-developer", "skill_slug": "react", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "full-stack-developer", "skill_slug": "tailwind-css", "required_level": 3, "importance": "medium", "is_core": False},
    {"career_slug": "full-stack-developer", "skill_slug": "nodejs", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "full-stack-developer", "skill_slug": "expressjs", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "full-stack-developer", "skill_slug": "fastapi", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "full-stack-developer", "skill_slug": "rest-api-design", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "full-stack-developer", "skill_slug": "relational-databases", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "full-stack-developer", "skill_slug": "postgresql", "required_level": 3, "importance": "high", "is_core": True},
    {"career_slug": "full-stack-developer", "skill_slug": "git-github", "required_level": 4, "importance": "critical", "is_core": True},
    {"career_slug": "full-stack-developer", "skill_slug": "docker", "required_level": 3, "importance": "medium", "is_core": False}
]
