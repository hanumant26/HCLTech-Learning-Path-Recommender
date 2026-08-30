"""
Canonical Technical Skills Taxonomy (95 Skills across 15 Domains).
"""

SKILLS_DATA = [
    # 1. Programming Languages
    {"slug": "python", "name": "Python", "category": "Programming Language", "description": "High-level programming language widely used in Data Science, AI, Web Development, and Automation."},
    {"slug": "r", "name": "R Programming", "category": "Programming Language", "description": "Programming language specialized for statistical computing and data visualization."},
    {"slug": "sql", "name": "SQL", "category": "Programming Language", "description": "Domain-specific language used for managing data in relational database management systems."},
    {"slug": "javascript", "name": "JavaScript", "category": "Programming Language", "description": "Core web scripting language enabling interactive web applications on client and server."},
    {"slug": "typescript", "name": "TypeScript", "category": "Programming Language", "description": "Strongly typed superset of JavaScript that compiles to plain JavaScript for scalable applications."},
    {"slug": "html-css", "name": "HTML & CSS", "category": "Programming Language", "description": "Standard markup and styling languages for constructing web pages and visual user interfaces."},
    {"slug": "java", "name": "Java", "category": "Programming Language", "description": "Class-based object-oriented language for enterprise applications and backend services."},
    {"slug": "cpp", "name": "C++", "category": "Programming Language", "description": "High-performance language used for systems programming, game engines, and low-level ML runtimes."},
    {"slug": "bash-shell", "name": "Bash & Shell Scripting", "category": "Programming Language", "description": "Command-line shell and scripting language for task automation in Unix/Linux environments."},

    # 2. Data Science & Wrangling
    {"slug": "pandas", "name": "Pandas", "category": "Data Science", "description": "Python library providing high-performance data structures and data analysis tools for tabular data."},
    {"slug": "numpy", "name": "NumPy", "category": "Data Science", "description": "Fundamental package for scientific computing in Python, providing multi-dimensional array objects."},
    {"slug": "exploratory-data-analysis", "name": "Exploratory Data Analysis", "category": "Data Science", "description": "Approach to analyzing data sets to summarize their main characteristics with visual methods."},
    {"slug": "data-cleaning", "name": "Data Cleaning & Preprocessing", "category": "Data Science", "description": "Techniques for detecting and correcting corrupt, incomplete, or inaccurate records in datasets."},
    {"slug": "data-visualization", "name": "Data Visualization", "category": "Data Science", "description": "Graphical representation of information and data to communicate insights clearly and effectively."},
    {"slug": "matplotlib-seaborn", "name": "Matplotlib & Seaborn", "category": "Data Science", "description": "Core Python libraries for generating static, animated, and interactive statistical graphics."},
    {"slug": "scipy", "name": "SciPy", "category": "Data Science", "description": "Python library used for scientific and technical computing including optimization and signal processing."},

    # 3. Statistics
    {"slug": "descriptive-statistics", "name": "Descriptive Statistics", "category": "Statistics", "description": "Quantitative summary of features of a dataset, including measures of central tendency and dispersion."},
    {"slug": "inferential-statistics", "name": "Inferential Statistics", "category": "Statistics", "description": "Methods for drawing conclusions and making predictions about populations based on sample data."},
    {"slug": "probability-theory", "name": "Probability Theory", "category": "Statistics", "description": "Mathematical study of random events, probability distributions, random variables, and expectation."},
    {"slug": "hypothesis-testing", "name": "Hypothesis Testing", "category": "Statistics", "description": "Statistical inference method used to decide whether sample evidence supports a specific hypothesis."},
    {"slug": "bayesian-statistics", "name": "Bayesian Statistics", "category": "Statistics", "description": "Theory of probability where evidence about the true state of the world is expressed in degrees of belief."},

    # 4. Mathematics
    {"slug": "linear-algebra", "name": "Linear Algebra", "category": "Mathematics", "description": "Branch of mathematics concerning linear equations, vector spaces, matrices, and matrix decompositions."},
    {"slug": "multivariable-calculus", "name": "Multivariable Calculus", "category": "Mathematics", "description": "Extension of calculus to functions of multiple variables, covering partial derivatives and gradients."},
    {"slug": "optimization-methods", "name": "Optimization Methods", "category": "Mathematics", "description": "Techniques such as Gradient Descent used to find optimal parameters that minimize cost functions."},
    {"slug": "discrete-mathematics", "name": "Discrete Mathematics", "category": "Mathematics", "description": "Study of mathematical structures that are countable, fundamental to computer science logic and graphs."},

    # 5. Machine Learning
    {"slug": "machine-learning-fundamentals", "name": "Machine Learning Fundamentals", "category": "Machine Learning", "description": "Core concepts of learning algorithms, generalization, bias-variance tradeoff, and overfitting."},
    {"slug": "supervised-learning", "name": "Supervised Learning", "category": "Machine Learning", "description": "ML algorithms trained on labeled datasets including Linear Regression, Decision Trees, and SVMs."},
    {"slug": "unsupervised-learning", "name": "Unsupervised Learning", "category": "Machine Learning", "description": "ML algorithms that infer patterns from unlabeled data including Clustering (K-Means) and PCA."},
    {"slug": "scikit-learn", "name": "Scikit-Learn", "category": "Machine Learning", "description": "Python module for machine learning built on top of NumPy, SciPy, and Matplotlib."},
    {"slug": "feature-engineering", "name": "Feature Engineering", "category": "Machine Learning", "description": "Process of using domain knowledge to extract features that make machine learning algorithms work better."},
    {"slug": "model-evaluation", "name": "Model Evaluation & Metrics", "category": "Machine Learning", "description": "Assessing model performance using Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Cross-Validation."},
    {"slug": "ensemble-learning", "name": "Ensemble Learning", "category": "Machine Learning", "description": "Combining multiple machine learning models to produce improved predictive performance (Bagging, Boosting)."},
    {"slug": "xgboost-lightgbm", "name": "XGBoost & LightGBM", "category": "Machine Learning", "description": "Gradient boosting frameworks optimized for high speed, performance, and tabular data competitive ML."},
    {"slug": "time-series-analysis", "name": "Time Series Analysis", "category": "Machine Learning", "description": "Methods for analyzing time series data to extract meaningful statistics and forecast future values."},
    {"slug": "reinforcement-learning", "name": "Reinforcement Learning", "category": "Machine Learning", "description": "Area of ML concerned with how intelligent agents take actions in an environment to maximize cumulative reward."},

    # 6. Deep Learning
    {"slug": "deep-learning-fundamentals", "name": "Deep Learning Fundamentals", "category": "Deep Learning", "description": "Concepts of artificial neural networks, activation functions, loss functions, and backpropagation."},
    {"slug": "neural-networks", "name": "Neural Networks", "category": "Deep Learning", "description": "Computing systems inspired by biological neural networks, forming the foundation of modern deep learning."},
    {"slug": "pytorch", "name": "PyTorch", "category": "Deep Learning", "description": "Open-source machine learning framework based on Torch, widely used for deep learning research and deployment."},
    {"slug": "tensorflow-keras", "name": "TensorFlow & Keras", "category": "Deep Learning", "description": "End-to-end open-source machine learning platform and high-level neural networks API."},
    {"slug": "cnn", "name": "Convolutional Neural Networks", "category": "Deep Learning", "description": "Class of deep neural networks designed for analyzing visual imagery and spatial grid structured data."},
    {"slug": "rnn-lstm", "name": "Recurrent Neural Networks & LSTM", "category": "Deep Learning", "description": "Neural network architectures designed for sequential data processing such as speech and time series."},
    {"slug": "transformers", "name": "Transformers Architecture", "category": "Deep Learning", "description": "Self-attention based neural network architecture powering modern state-of-the-art NLP and vision models."},
    {"slug": "model-deployment", "name": "Model Deployment", "category": "Machine Learning", "description": "Packaging machine learning models as production REST APIs or microservices using Docker and FastAPI."},

    # 7. Natural Language Processing (NLP)
    {"slug": "nlp-fundamentals", "name": "NLP Fundamentals", "category": "NLP", "description": "Core concepts of natural language processing including NLTK, spaCy, and text normalization."},
    {"slug": "text-preprocessing", "name": "Text Preprocessing & Tokenization", "category": "NLP", "description": "Techniques for cleaning, stemming, lemmatizing, and tokenizing raw natural language text data."},
    {"slug": "word-embeddings", "name": "Word Embeddings", "category": "NLP", "description": "Vector representations of words capturing semantic relationships (Word2Vec, GloVe, FastText)."},
    {"slug": "large-language-models", "name": "Large Language Models", "category": "NLP", "description": "Pre-trained transformer models fine-tuned for text generation, comprehension, and reasoning tasks."},
    {"slug": "prompt-engineering", "name": "Prompt Engineering", "category": "NLP", "description": "Structuring textual queries to effectively communicate with and guide Large Language Models."},
    {"slug": "retrieval-augmented-generation", "name": "Retrieval-Augmented Generation", "category": "NLP", "description": "Architecture combining vector search retrieval with generative LLMs to answer queries using domain data."},
    {"slug": "langchain", "name": "LangChain & AI Frameworks", "category": "NLP", "description": "Framework for developing applications powered by language models and agentic workflows."},

    # 8. Computer Vision
    {"slug": "computer-vision-fundamentals", "name": "Computer Vision Fundamentals", "category": "Computer Vision", "description": "Core techniques for acquiring, processing, analyzing, and understanding digital images."},
    {"slug": "opencv", "name": "OpenCV", "category": "Computer Vision", "description": "Open-source computer vision and machine learning software library for real-time image processing."},
    {"slug": "image-processing", "name": "Image Processing", "category": "Computer Vision", "description": "Operations on digital images including filtering, edge detection, transformations, and color spaces."},
    {"slug": "object-detection", "name": "Object Detection", "category": "Computer Vision", "description": "Computer vision technique for identifying and locating instances of objects within images (YOLO, R-CNN)."},
    {"slug": "image-segmentation", "name": "Image Segmentation", "category": "Computer Vision", "description": "Partitioning a digital image into multiple segments (pixels) to simplify image analysis."},

    # 9. Databases & Data Warehousing
    {"slug": "relational-databases", "name": "Relational Databases", "category": "Databases", "description": "Database systems based on the relational model of data organizing information into tables."},
    {"slug": "postgresql", "name": "PostgreSQL", "category": "Databases", "description": "Advanced, open-source object-relational database system known for reliability, robustness, and performance."},
    {"slug": "mysql", "name": "MySQL", "category": "Databases", "description": "Popular open-source relational database management system widely used in web application stacks."},
    {"slug": "nosql-databases", "name": "NoSQL Databases", "category": "Databases", "description": "Non-relational database systems optimized for flexible data models, key-value, document, or graph stores."},
    {"slug": "mongodb", "name": "MongoDB", "category": "Databases", "description": "Source-available document-oriented database program classified as a NoSQL database system."},
    {"slug": "redis", "name": "Redis", "category": "Databases", "description": "In-memory data structure store used as a database, cache, streaming engine, and message broker."},
    {"slug": "database-indexing", "name": "Database Indexing & Optimization", "category": "Databases", "description": "Strategies for optimizing query performance through indexes, query execution plans, and partitioning."},
    {"slug": "data-modeling", "name": "Data Modeling & Schema Design", "category": "Databases", "description": "Process of creating a data model for information systems by applying formal data modeling techniques."},

    # 10. Web & Frontend Development
    {"slug": "web-fundamentals", "name": "Web Fundamentals", "category": "Web Development", "description": "Foundational web architecture principles including HTTP protocols, DNS, DOM, and browser rendering."},
    {"slug": "react", "name": "React", "category": "Frontend Development", "description": "Declarative component-based JavaScript library for building modern web user interfaces."},
    {"slug": "nextjs", "name": "Next.js", "category": "Frontend Development", "description": "React framework enabling server-side rendering, static site generation, and full-stack web applications."},
    {"slug": "vuejs", "name": "Vue.js", "category": "Frontend Development", "description": "Progressive JavaScript framework for building user interfaces and single-page applications."},
    {"slug": "tailwind-css", "name": "Tailwind CSS", "category": "Frontend Development", "description": "Utility-first CSS framework for rapidly building custom modern responsive user interfaces."},
    {"slug": "state-management", "name": "State Management", "category": "Frontend Development", "description": "Patterns and libraries for managing complex state across frontend components (Redux, Zustand, Context API)."},
    {"slug": "responsive-design", "name": "Responsive Web Design", "category": "Frontend Development", "description": "Approach to web design making web pages render well on a variety of devices and window screen sizes."},

    # 11. Backend Development
    {"slug": "fastapi", "name": "FastAPI", "category": "Backend Development", "description": "Modern, fast, high-performance web framework for building APIs with Python based on standard type hints."},
    {"slug": "flask", "name": "Flask", "category": "Backend Development", "description": "Micro web framework written in Python designed to make getting started quick and easy."},
    {"slug": "django", "name": "Django", "category": "Backend Development", "description": "High-level Python web framework that encourages rapid development and clean pragmatic design."},
    {"slug": "nodejs", "name": "Node.js", "category": "Backend Development", "description": "Cross-platform JavaScript runtime environment executing JavaScript code outside a web browser."},
    {"slug": "expressjs", "name": "Express.js", "category": "Backend Development", "description": "Minimal and flexible Node.js web application framework providing a robust set of features for APIs."},
    {"slug": "rest-api-design", "name": "REST API Design", "category": "Backend Development", "description": "Architectural principles for designing scalable stateless web services and HTTP API endpoints."},
    {"slug": "graphql", "name": "GraphQL", "category": "Backend Development", "description": "Query language for APIs and runtime for fulfilling queries with existing data."},

    # 12. Software Engineering Principles
    {"slug": "object-oriented-programming", "name": "Object-Oriented Programming", "category": "Software Engineering", "description": "Programming paradigm based on the concept of objects containing data and code (Encapsulation, Inheritance, Polymorphism)."},
    {"slug": "functional-programming", "name": "Functional Programming", "category": "Software Engineering", "description": "Programming paradigm treating computation as the evaluation of mathematical functions avoiding state mutation."},
    {"slug": "software-design-patterns", "name": "Software Design Patterns", "category": "Software Engineering", "description": "Reusable solutions to commonly occurring software design problems (Factory, Singleton, Observer, Decorator)."},
    {"slug": "unit-testing", "name": "Unit Testing & TDD", "category": "Software Engineering", "description": "Software testing methodology where individual units of code are tested, driven by Test-Driven Development."},
    {"slug": "system-design", "name": "System Design & Architecture", "category": "Software Engineering", "description": "Process of defining the architecture, components, modules, interfaces, and data for a system to satisfy specified requirements."},

    # 13. Tools, Git & Version Control
    {"slug": "git-github", "name": "Git & GitHub", "category": "Tools & Version Control", "description": "Distributed version control system and cloud platform for tracking code changes and team collaboration."},

    # 14. DevOps & Cloud Basics
    {"slug": "docker", "name": "Docker & Containerization", "category": "DevOps & Cloud", "description": "OS-level virtualization deliver software in packages called containers isolating app code and dependencies."},
    {"slug": "kubernetes", "name": "Kubernetes", "category": "DevOps & Cloud", "description": "Open-source container orchestration system for automating application deployment, scaling, and management."},
    {"slug": "ci-cd", "name": "CI/CD Pipelines", "category": "DevOps & Cloud", "description": "Automated pipeline for Continuous Integration and Continuous Deployment of code releases."},
    {"slug": "cloud-computing-basics", "name": "Cloud Computing Basics", "category": "DevOps & Cloud", "description": "Foundational principles of cloud computing including IaaS, PaaS, SaaS, elasticity, and virtual networks."},
    {"slug": "aws-basics", "name": "AWS Cloud Services", "category": "DevOps & Cloud", "description": "Amazon Web Services cloud computing platform including EC2, S3, IAM, and Lambda."},
    {"slug": "azure-basics", "name": "Azure Cloud Services", "category": "DevOps & Cloud", "description": "Microsoft Azure cloud services ecosystem for computing, analytics, storage, and networking."},
    {"slug": "linux-fundamentals", "name": "Linux Fundamentals", "category": "DevOps & Cloud", "description": "Core operating system principles, file permissions, terminal commands, and process management in Linux."},

    # 15. Analytics & Business Intelligence
    {"slug": "power-bi", "name": "Power BI", "category": "Analytics & BI", "description": "Interactive data visualization software product developed by Microsoft with a primary focus on business intelligence."},
    {"slug": "tableau", "name": "Tableau", "category": "Analytics & BI", "description": "Interactive data visualization software focused on business intelligence and analytics dashboards."},
    {"slug": "excel-advanced", "name": "Advanced Excel", "category": "Analytics & BI", "description": "Advanced spreadsheet calculations, VLOOKUP/XLOOKUP, Pivot Tables, and financial/statistical data analysis."},
    {"slug": "data-warehousing", "name": "Data Warehousing", "category": "Analytics & BI", "description": "Central repositories of integrated data from one or more disparate sources (Snowflake, BigQuery, Redshift)."},
    {"slug": "etl-pipelines", "name": "ETL & Data Pipelines", "category": "Analytics & BI", "description": "Extract, Transform, Load processes for building reliable automated data processing pipelines."}
]
