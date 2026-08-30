"""
Diagnostic Assessment Datasets for Major Skills (Python, SQL, Statistics, ML, Deep Learning, JS, React, Node.js).
Each assessment contains 5 structured multiple-choice questions with options, correct answer, difficulty, and skill tested.
"""

ASSESSMENTS_DATA = [
    {
        "skill_slug": "python",
        "title": "Python Programming Proficiency Diagnostic",
        "description": "Evaluates core Python syntax, data structures, list comprehensions, object-oriented concepts, and memory management.",
        "passing_score_pct": 70.0,
        "questions": [
            {
                "question": "What is the output of `[x**2 for x in range(5) if x % 2 == 0]` in Python?",
                "options": ["[0, 4, 16]", "[0, 1, 4, 9, 16]", "[0, 4]", "[4, 16]"],
                "correct_answer": "[0, 4, 16]",
                "difficulty": "beginner",
                "skill_tested": "python"
            },
            {
                "question": "Which of the following data structures in Python is immutable?",
                "options": ["List", "Dictionary", "Tuple", "Set"],
                "correct_answer": "Tuple",
                "difficulty": "beginner",
                "skill_tested": "python"
            },
            {
                "question": "How does Python handle memory management for unused objects?",
                "options": ["Manual deallocation using free()", "Automatic garbage collection via reference counting and generational GC", "Stack allocation only", "Requires explicit delete keywords for all variables"],
                "correct_answer": "Automatic garbage collection via reference counting and generational GC",
                "difficulty": "intermediate",
                "skill_tested": "python"
            },
            {
                "question": "What keyword is used to create a generator function in Python?",
                "options": ["return", "yield", "generate", "async"],
                "correct_answer": "yield",
                "difficulty": "intermediate",
                "skill_tested": "python"
            },
            {
                "question": "In Python, what is the main purpose of the `*args` and `**kwargs` parameters in a function definition?",
                "options": ["To pass type annotations", "To accept an arbitrary number of positional and keyword arguments", "To enable multithreading", "To speed up function execution"],
                "correct_answer": "To accept an arbitrary number of positional and keyword arguments",
                "difficulty": "intermediate",
                "skill_tested": "python"
            }
        ]
    },
    {
        "skill_slug": "sql",
        "title": "SQL & Relational Query Diagnostic",
        "description": "Evaluates SELECT queries, JOIN types, GROUP BY aggregations, window functions, and indexing concepts.",
        "passing_score_pct": 70.0,
        "questions": [
            {
                "question": "Which SQL JOIN returns all rows from the left table and matched records from the right table?",
                "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"],
                "correct_answer": "LEFT JOIN",
                "difficulty": "beginner",
                "skill_tested": "sql"
            },
            {
                "question": "What is the difference between WHERE and HAVING clauses in SQL?",
                "options": ["WHERE filters aggregated results; HAVING filters rows before grouping", "WHERE filters rows before aggregation; HAVING filters groups after GROUP BY", "They are completely identical in function", "HAVING can only be used with subqueries"],
                "correct_answer": "WHERE filters rows before aggregation; HAVING filters groups after GROUP BY",
                "difficulty": "intermediate",
                "skill_tested": "sql"
            },
            {
                "question": "Which SQL window function assigns a unique sequential integer to rows starting at 1 within a partition?",
                "options": ["RANK()", "DENSE_RANK()", "ROW_NUMBER()", "NTILE()"],
                "correct_answer": "ROW_NUMBER()",
                "difficulty": "intermediate",
                "skill_tested": "sql"
            },
            {
                "question": "What is the primary benefit of creating a B-Tree index on a database column?",
                "options": ["Reduces table storage space", "Accelerates search and query lookup time from O(N) to O(log N)", "Prevents NULL values from being inserted", "Automatically encrypts column data"],
                "correct_answer": "Accelerates search and query lookup time from O(N) to O(log N)",
                "difficulty": "intermediate",
                "skill_tested": "sql"
            },
            {
                "question": "Which SQL statement is used to remove all records from a table without logging individual row deletions?",
                "options": ["DELETE FROM table", "TRUNCATE TABLE table", "DROP TABLE table", "REMOVE TABLE table"],
                "correct_answer": "TRUNCATE TABLE table",
                "difficulty": "intermediate",
                "skill_tested": "sql"
            }
        ]
    },
    {
        "skill_slug": "descriptive-statistics",
        "title": "Statistics & Probability Diagnostic",
        "description": "Evaluates probability distributions, central limit theorem, hypothesis testing, and confidence intervals.",
        "passing_score_pct": 70.0,
        "questions": [
            {
                "question": "According to the Central Limit Theorem, what distribution does the sample mean approach as sample size increases?",
                "options": ["Uniform Distribution", "Normal Distribution", "Exponential Distribution", "Binomial Distribution"],
                "correct_answer": "Normal Distribution",
                "difficulty": "intermediate",
                "skill_tested": "descriptive-statistics"
            },
            {
                "question": "What does a p-value less than 0.05 signify in hypothesis testing?",
                "options": ["The null hypothesis is true", "Statistically significant evidence against the null hypothesis", "The alternative hypothesis is false", "The sample size is too small"],
                "correct_answer": "Statistically significant evidence against the null hypothesis",
                "difficulty": "intermediate",
                "skill_tested": "descriptive-statistics"
            },
            {
                "question": "Which measure of central tendency is most robust to extreme outliers?",
                "options": ["Mean", "Median", "Variance", "Standard Deviation"],
                "correct_answer": "Median",
                "difficulty": "beginner",
                "skill_tested": "descriptive-statistics"
            },
            {
                "question": "What is a Type I error in statistical hypothesis testing?",
                "options": ["Failing to reject a false null hypothesis", "Rejecting a true null hypothesis (False Positive)", "Calculating incorrect sample mean", "Selecting a non-random sample"],
                "correct_answer": "Rejecting a true null hypothesis (False Positive)",
                "difficulty": "intermediate",
                "skill_tested": "descriptive-statistics"
            },
            {
                "question": "If two events A and B are independent, how is P(A and B) calculated?",
                "options": ["P(A) + P(B)", "P(A) * P(B)", "P(A) / P(B)", "P(A) - P(B)"],
                "correct_answer": "P(A) * P(B)",
                "difficulty": "beginner",
                "skill_tested": "descriptive-statistics"
            }
        ]
    },
    {
        "skill_slug": "machine-learning-fundamentals",
        "title": "Machine Learning Fundamentals Diagnostic",
        "description": "Evaluates supervised/unsupervised learning concepts, bias-variance tradeoff, cross-validation, and metrics.",
        "passing_score_pct": 70.0,
        "questions": [
            {
                "question": "What condition occurs when a machine learning model performs exceptionally on training data but fails to generalize to unseen test data?",
                "options": ["Underfitting", "Overfitting", "High Bias", "Linear Collapsibility"],
                "correct_answer": "Overfitting",
                "difficulty": "beginner",
                "skill_tested": "machine-learning-fundamentals"
            },
            {
                "question": "Which metric is preferable over Accuracy for evaluating classification models on highly imbalanced datasets?",
                "options": ["Mean Squared Error", "F1-Score / ROC-AUC", "R-Squared", "Mean Absolute Error"],
                "correct_answer": "F1-Score / ROC-AUC",
                "difficulty": "intermediate",
                "skill_tested": "machine-learning-fundamentals"
            },
            {
                "question": "In L1 Regularization (Lasso), what effect does the penalty term have on model coefficients?",
                "options": ["Shrinks all coefficients proportionally without reaching zero", "Drives irrelevant feature coefficients exactly to zero (Feature Selection)", "Multiplies coefficients by learning rate", "Prevents model convergence"],
                "correct_answer": "Drives irrelevant feature coefficients exactly to zero (Feature Selection)",
                "difficulty": "intermediate",
                "skill_tested": "machine-learning-fundamentals"
            },
            {
                "question": "Which algorithm is an example of an Unsupervised Learning method?",
                "options": ["Logistic Regression", "K-Means Clustering", "Random Forest Classifier", "Support Vector Machine"],
                "correct_answer": "K-Means Clustering",
                "difficulty": "beginner",
                "skill_tested": "machine-learning-fundamentals"
            },
            {
                "question": "What is the primary purpose of K-Fold Cross-Validation?",
                "options": ["To speed up model training time", "To get a reliable, unbiased estimate of model performance across data splits", "To clean missing data values", "To reduce dataset dimensionality"],
                "correct_answer": "To get a reliable, unbiased estimate of model performance across data splits",
                "difficulty": "intermediate",
                "skill_tested": "machine-learning-fundamentals"
            }
        ]
    },
    {
        "skill_slug": "deep-learning-fundamentals",
        "title": "Deep Learning & Neural Networks Diagnostic",
        "description": "Evaluates neural network architectures, backpropagation, activation functions, and optimizer mechanics.",
        "passing_score_pct": 70.0,
        "questions": [
            {
                "question": "Why is the ReLU (Rectified Linear Unit) activation function widely used in deep neural networks over Sigmoid?",
                "options": ["It bounds outputs strictly between -1 and 1", "It mitigates the vanishing gradient problem in deep hidden layers", "It eliminates the need for backpropagation", "It requires matrix inversion"],
                "correct_answer": "It mitigates the vanishing gradient problem in deep hidden layers",
                "difficulty": "intermediate",
                "skill_tested": "deep-learning-fundamentals"
            },
            {
                "question": "What algorithm calculates the gradient of the loss function with respect to each weight in a neural network using the chain rule?",
                "options": ["Forward Propagation", "Backpropagation", "Gradient Ascent", "K-Means Partitioning"],
                "correct_answer": "Backpropagation",
                "difficulty": "beginner",
                "skill_tested": "deep-learning-fundamentals"
            },
            {
                "question": "What is the primary function of a Dropout layer in a deep learning model?",
                "options": ["To normalize batch inputs", "To randomly deactivate a fraction of neurons during training to prevent overfitting", "To accelerate matrix multiplication", "To increase model parameter count"],
                "correct_answer": "To randomly deactivate a fraction of neurons during training to prevent overfitting",
                "difficulty": "intermediate",
                "skill_tested": "deep-learning-fundamentals"
            },
            {
                "question": "Which architecture component allows Transformer models to process all tokens in a sequence concurrently?",
                "options": ["Recurrent Gates", "Self-Attention Mechanism", "Pooling Layers", "Convolution Kernels"],
                "correct_answer": "Self-Attention Mechanism",
                "difficulty": "advanced",
                "skill_tested": "deep-learning-fundamentals"
            },
            {
                "question": "What type of neural network layer is specifically designed for spatial feature extraction in images?",
                "options": ["Dense Layer", "Convolutional Layer (CNN)", "LSTM Layer", "Embedding Layer"],
                "correct_answer": "Convolutional Layer (CNN)",
                "difficulty": "beginner",
                "skill_tested": "deep-learning-fundamentals"
            }
        ]
    },
    {
        "skill_slug": "javascript",
        "title": "JavaScript Core Concepts Diagnostic",
        "description": "Evaluates JS closures, scope, promises, async/await, DOM event loop, and ES6 features.",
        "passing_score_pct": 70.0,
        "questions": [
            {
                "question": "What is a closure in JavaScript?",
                "options": ["A function bundled together with references to its surrounding state (lexical environment)", "A method to close browser tabs programmatically", "A syntax for terminating loops early", "A strictly private object class"],
                "correct_answer": "A function bundled together with references to its surrounding state (lexical environment)",
                "difficulty": "intermediate",
                "skill_tested": "javascript"
            },
            {
                "question": "What is the result of `typeof null` in JavaScript?",
                "options": ["\"null\"", "\"undefined\"", "\"object\"", "\"boolean\""],
                "correct_answer": "\"object\"",
                "difficulty": "beginner",
                "skill_tested": "javascript"
            },
            {
                "question": "Which keyword declares a block-scoped variable that cannot be re-assigned?",
                "options": ["var", "let", "const", "static"],
                "correct_answer": "const",
                "difficulty": "beginner",
                "skill_tested": "javascript"
            },
            {
                "question": "How does the JavaScript event loop handle asynchronous tasks like `setTimeout`?",
                "options": ["Executes them immediately on a parallel CPU thread", "Places callbacks in the Task Queue, executing them once the Call Stack is empty", "Suspends all synchronous execution until timer finishes", "Transpiles them into synchronous while loops"],
                "correct_answer": "Places callbacks in the Task Queue, executing them once the Call Stack is empty",
                "difficulty": "intermediate",
                "skill_tested": "javascript"
            },
            {
                "question": "What does the `Promise.all()` method do when passed an array of promises?",
                "options": ["Resolves when the first promise resolves", "Resolves when all promises resolve, or rejects immediately if any promise fails", "Executes promises sequentially one after another", "Ignores rejected promises"],
                "correct_answer": "Resolves when all promises resolve, or rejects immediately if any promise fails",
                "difficulty": "intermediate",
                "skill_tested": "javascript"
            }
        ]
    },
    {
        "skill_slug": "react",
        "title": "React Architecture & Hooks Diagnostic",
        "description": "Evaluates React functional components, hooks lifecycle, virtual DOM, props vs state, and re-rendering rules.",
        "passing_score_pct": 70.0,
        "questions": [
            {
                "question": "Which React hook is used to handle side effects such as data fetching or subscriptions?",
                "options": ["useState", "useEffect", "useContext", "useReducer"],
                "correct_answer": "useEffect",
                "difficulty": "beginner",
                "skill_tested": "react"
            },
            {
                "question": "What triggers a React component to re-render?",
                "options": ["A change in props or state", "Navigating the DOM tree manually", "Calling console.log()", "Declaring a new local variable"],
                "correct_answer": "A change in props or state",
                "difficulty": "beginner",
                "skill_tested": "react"
            },
            {
                "question": "Why should keys be provided when rendering lists of elements in React?",
                "options": ["To style list items with CSS", "To help React identify which items have changed, been added, or removed efficiently", "Keys are required by JavaScript engines", "To prevent memory leaks in state"],
                "correct_answer": "To help React identify which items have changed, been added, or removed efficiently",
                "difficulty": "intermediate",
                "skill_tested": "react"
            },
            {
                "question": "What is the Virtual DOM in React?",
                "options": ["A physical browser window extension", "An in-memory lightweight representation of the real DOM used for reconciliation", "A backend server database engine", "A CSS preprocessor"],
                "correct_answer": "An in-memory lightweight representation of the real DOM used for reconciliation",
                "difficulty": "intermediate",
                "skill_tested": "react"
            },
            {
                "question": "Which hook optimizes performance by memoizing expensive calculation results between renders?",
                "options": ["useCallback", "useMemo", "useRef", "useImperativeHandle"],
                "correct_answer": "useMemo",
                "difficulty": "intermediate",
                "skill_tested": "react"
            }
        ]
    },
    {
        "skill_slug": "nodejs",
        "title": "Node.js & Backend Architecture Diagnostic",
        "description": "Evaluates Node.js non-blocking I/O, event loop, Express middleware, streams, and module system.",
        "passing_score_pct": 70.0,
        "questions": [
            {
                "question": "What architecture enables Node.js to handle thousands of concurrent requests efficiently?",
                "options": ["Multi-threaded synchronous blocking I/O", "Single-threaded event loop with non-blocking I/O", "Process per connection model", "Hardware GPU threading"],
                "correct_answer": "Single-threaded event loop with non-blocking I/O",
                "difficulty": "intermediate",
                "skill_tested": "nodejs"
            },
            {
                "question": "In Express.js, what is middleware?",
                "options": ["A database indexing plugin", "Functions that have access to request and response objects and call next() to yield control", "A frontend UI library", "A build bundler"],
                "correct_answer": "Functions that have access to request and response objects and call next() to yield control",
                "difficulty": "beginner",
                "skill_tested": "nodejs"
            },
            {
                "question": "Which Node.js core module is used to work with file paths across operating systems?",
                "options": ["fs", "path", "http", "events"],
                "correct_answer": "path",
                "difficulty": "beginner",
                "skill_tested": "nodejs"
            },
            {
                "question": "What is the purpose of `package.json` in a Node.js project?",
                "options": ["Configures database connection credentials", "Manifest file holding project metadata, scripts, and dependency definitions", "Contains compiled C++ binaries", "Defines HTML page structure"],
                "correct_answer": "Manifest file holding project metadata, scripts, and dependency definitions",
                "difficulty": "beginner",
                "skill_tested": "nodejs"
            },
            {
                "question": "What method is used to stream large files without loading the entire content into RAM in Node.js?",
                "options": ["fs.readFileSync()", "fs.createReadStream()", "fs.writeFileSync()", "fs.appendFileSync()"],
                "correct_answer": "fs.createReadStream()",
                "difficulty": "intermediate",
                "skill_tested": "nodejs"
            }
        ]
    }
]
