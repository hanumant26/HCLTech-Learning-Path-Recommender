"""
Skill Prerequisites Graph Dataset (Directed Acyclic Graph).
Each entry: (skill_slug, prerequisite_slug, required_level)
Meaning: skill_slug requires prerequisite_slug at required_level.
"""

PREREQUISITES_DATA = [
    # Data Science & Math
    ("pandas", "python", 2),
    ("numpy", "python", 2),
    ("exploratory-data-analysis", "pandas", 2),
    ("exploratory-data-analysis", "numpy", 2),
    ("data-cleaning", "pandas", 2),
    ("matplotlib-seaborn", "python", 2),
    ("matplotlib-seaborn", "pandas", 1),
    ("scipy", "numpy", 2),

    # Statistics
    ("inferential-statistics", "descriptive-statistics", 2),
    ("hypothesis-testing", "inferential-statistics", 2),
    ("probability-theory", "descriptive-statistics", 2),
    ("bayesian-statistics", "probability-theory", 2),

    # Mathematics
    ("multivariable-calculus", "linear-algebra", 1),
    ("optimization-methods", "multivariable-calculus", 2),

    # Machine Learning
    ("machine-learning-fundamentals", "python", 2),
    ("machine-learning-fundamentals", "descriptive-statistics", 2),
    ("supervised-learning", "machine-learning-fundamentals", 2),
    ("supervised-learning", "python", 2),
    ("unsupervised-learning", "machine-learning-fundamentals", 2),
    ("scikit-learn", "python", 2),
    ("scikit-learn", "pandas", 2),
    ("scikit-learn", "supervised-learning", 2),
    ("feature-engineering", "pandas", 2),
    ("model-evaluation", "supervised-learning", 2),
    ("ensemble-learning", "supervised-learning", 2),
    ("xgboost-lightgbm", "ensemble-learning", 2),
    ("time-series-analysis", "pandas", 2),
    ("time-series-analysis", "descriptive-statistics", 2),

    # Deep Learning
    ("deep-learning-fundamentals", "machine-learning-fundamentals", 2),
    ("deep-learning-fundamentals", "linear-algebra", 1),
    ("neural-networks", "deep-learning-fundamentals", 2),
    ("pytorch", "python", 3),
    ("pytorch", "deep-learning-fundamentals", 2),
    ("tensorflow-keras", "python", 3),
    ("tensorflow-keras", "deep-learning-fundamentals", 2),
    ("cnn", "neural-networks", 2),
    ("rnn-lstm", "neural-networks", 2),
    ("transformers", "neural-networks", 2),

    # NLP
    ("nlp-fundamentals", "python", 2),
    ("text-preprocessing", "nlp-fundamentals", 2),
    ("word-embeddings", "text-preprocessing", 2),
    ("large-language-models", "transformers", 2),
    ("prompt-engineering", "large-language-models", 1),
    ("retrieval-augmented-generation", "large-language-models", 2),
    ("langchain", "python", 3),
    ("langchain", "large-language-models", 2),

    # Computer Vision
    ("computer-vision-fundamentals", "python", 2),
    ("opencv", "computer-vision-fundamentals", 2),
    ("image-processing", "opencv", 2),
    ("object-detection", "cnn", 2),
    ("image-segmentation", "cnn", 2),

    # Databases
    ("postgresql", "relational-databases", 2),
    ("mysql", "relational-databases", 2),
    ("mongodb", "nosql-databases", 2),
    ("redis", "nosql-databases", 1),
    ("database-indexing", "relational-databases", 2),
    ("database-indexing", "sql", 2),
    ("data-modeling", "relational-databases", 2),

    # Web & Frontend
    ("typescript", "javascript", 2),
    ("react", "javascript", 3),
    ("react", "html-css", 2),
    ("nextjs", "react", 3),
    ("vuejs", "javascript", 3),
    ("tailwind-css", "html-css", 2),
    ("state-management", "react", 3),

    # Backend
    ("nodejs", "javascript", 3),
    ("expressjs", "nodejs", 2),
    ("fastapi", "python", 3),
    ("flask", "python", 2),
    ("django", "python", 3),
    ("rest-api-design", "web-fundamentals", 2),
    ("graphql", "rest-api-design", 2),

    # DevOps, Cloud & Deployment
    ("docker", "linux-fundamentals", 2),
    ("kubernetes", "docker", 2),
    ("ci-cd", "git-github", 2),
    ("aws-basics", "cloud-computing-basics", 2),
    ("azure-basics", "cloud-computing-basics", 2),
    ("model-deployment", "docker", 2),
    ("model-deployment", "fastapi", 2),

    # BI & Analytics
    ("power-bi", "excel-advanced", 2),
    ("tableau", "excel-advanced", 2),
    ("etl-pipelines", "python", 2),
    ("etl-pipelines", "sql", 2),
    ("data-warehousing", "sql", 3)
]
