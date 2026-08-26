import {
  LearnerProfile,
  SkillLevel,
  Recommendation,
  RoadmapNode,
  ProgressSummary,
  Assessment,
  Course,
  ActivityEvent,
  CareerProfile,
  NotificationItem,
  Achievement,
  StreakInfo,
} from "../types";

export const mockProfile: LearnerProfile = {
  id: "user-1",
  name: "Aditi Sharma",
  careerGoal: "Data Scientist",
  weeklyHours: 8,
  experienceLevel: "Beginner",
  preferences: "Prefer hands-on projects over long video lectures",
};

export const mockSkills: SkillLevel[] = [
  { skillId: "s1", skillName: "Python", proficiency: 4, requiredForGoal: 5 },
  { skillId: "s2", skillName: "SQL", proficiency: 3, requiredForGoal: 4 },
  { skillId: "s3", skillName: "Statistics", proficiency: 2, requiredForGoal: 4 },
  { skillId: "s4", skillName: "Machine Learning", proficiency: 1, requiredForGoal: 5 },
  { skillId: "s5", skillName: "Data Visualization", proficiency: 2, requiredForGoal: 3 },
];

export const mockRecommendations: Recommendation[] = [
  {
    id: "r1",
    title: "Statistics for Data Science",
    type: "course",
    difficulty: "Beginner",
    estimatedHours: 12,
    skillsCovered: ["Statistics"],
    score: 92,
    reason: "Statistics is your largest skill gap for the Data Scientist path.",
    prerequisites: [],
    description:
      "A practical statistics course covering distributions, hypothesis testing, and regression fundamentals used throughout data science workflows.",
  },
  {
    id: "r2",
    title: "Intro to Machine Learning",
    type: "course",
    difficulty: "Beginner",
    estimatedHours: 18,
    skillsCovered: ["Machine Learning"],
    score: 88,
    reason: "Unlocks the ML track and directly targets your lowest-proficiency skill.",
    prerequisites: ["Statistics"],
    description:
      "Covers supervised and unsupervised learning, model evaluation, and scikit-learn basics with applied notebooks.",
  },
  {
    id: "r3",
    title: "SQL Query Practice Set",
    type: "practice",
    difficulty: "Intermediate",
    estimatedHours: 4,
    skillsCovered: ["SQL"],
    score: 76,
    reason: "Reinforces SQL to close the gap to your target proficiency of 4/5.",
    prerequisites: [],
    description:
      "A set of 25 progressively harder SQL queries against a retail dataset, with instant feedback.",
  },
  {
    id: "r4",
    title: "Exploratory Data Analysis Project",
    type: "project",
    difficulty: "Intermediate",
    estimatedHours: 10,
    skillsCovered: ["Data Visualization", "Statistics"],
    score: 71,
    reason: "Combines two skills you're building and produces a portfolio artifact.",
    prerequisites: ["Statistics for Data Science"],
    description:
      "Analyze a real-world dataset end-to-end and present findings with charts and a short written summary.",
  },
  {
    id: "r5",
    title: "ML Fundamentals Checkpoint",
    type: "assessment",
    difficulty: "Beginner",
    estimatedHours: 1,
    skillsCovered: ["Machine Learning"],
    score: 65,
    reason: "Validates readiness before moving to applied ML projects.",
    prerequisites: ["Intro to Machine Learning"],
    description: "A short quiz checking core ML vocabulary and concepts before you proceed.",
  },
];

export const mockRoadmap: RoadmapNode[] = [
  {
    id: "n1",
    title: "Python Refresher",
    type: "course",
    status: "completed",
    estimatedHours: 6,
    difficulty: "Beginner",
    missingPrerequisites: [],
    order: 1,
  },
  {
    id: "n2",
    title: "Statistics for Data Science",
    type: "course",
    status: "ready",
    estimatedHours: 12,
    difficulty: "Beginner",
    missingPrerequisites: [],
    order: 2,
  },
  {
    id: "n3",
    title: "SQL Query Practice Set",
    type: "practice",
    status: "ready",
    estimatedHours: 4,
    difficulty: "Intermediate",
    missingPrerequisites: [],
    order: 3,
  },
  {
    id: "n4",
    title: "Intro to Machine Learning",
    type: "course",
    status: "locked",
    estimatedHours: 18,
    difficulty: "Beginner",
    missingPrerequisites: ["Statistics for Data Science"],
    order: 4,
  },
  {
    id: "n5",
    title: "ML Fundamentals Checkpoint",
    type: "assessment",
    status: "locked",
    estimatedHours: 1,
    difficulty: "Beginner",
    missingPrerequisites: ["Intro to Machine Learning"],
    order: 5,
  },
  {
    id: "n6",
    title: "Exploratory Data Analysis Project",
    type: "project",
    status: "locked",
    estimatedHours: 10,
    difficulty: "Intermediate",
    missingPrerequisites: ["Statistics for Data Science"],
    order: 6,
  },
];

export const mockProgress: ProgressSummary = {
  overallPercent: 24,
  skillsDeveloped: 2,
  coursesCompleted: 1,
  projectsCompleted: 0,
  currentPhase: "Foundations",
  milestones: [
    { title: "Complete profile setup", done: true },
    { title: "Finish Python Refresher", done: true },
    { title: "Finish Statistics for Data Science", done: false },
    { title: "Pass ML Fundamentals Checkpoint", done: false },
    { title: "Ship first EDA project", done: false },
  ],
  nextAction: "Continue \"Statistics for Data Science\" — 12 hrs estimated",
};

export const careerOptions = [
  "Data Scientist",
  "AI Engineer",
  "Machine Learning Engineer",
  "Data Analyst",
  "Full Stack Developer",
] as const;

// Keyed by resource id "r5" / roadmap node id "n5" — both represent the same
// "ML Fundamentals Checkpoint" assessment, so ResourceDetails can link to
// /assessment/r5 or /assessment/n5 and get the same quiz.
export const mockAssessments: Record<string, Assessment> = {
  r5: {
    id: "r5",
    title: "ML Fundamentals Checkpoint",
    skillsTested: ["Machine Learning"],
    passingScorePercent: 70,
    questions: [
      {
        id: "q1",
        prompt: "What is the main difference between supervised and unsupervised learning?",
        options: [
          { id: "a", text: "Supervised learning uses labeled data; unsupervised does not" },
          { id: "b", text: "Supervised learning is always faster to train" },
          { id: "c", text: "Unsupervised learning requires a GPU" },
          { id: "d", text: "There is no meaningful difference" },
        ],
        correctOptionId: "a",
      },
      {
        id: "q2",
        prompt: "Which metric is most appropriate for evaluating a classifier on an imbalanced dataset?",
        options: [
          { id: "a", text: "Raw accuracy" },
          { id: "b", text: "F1 score" },
          { id: "c", text: "Mean squared error" },
          { id: "d", text: "R-squared" },
        ],
        correctOptionId: "b",
      },
      {
        id: "q3",
        prompt: "What does 'overfitting' mean?",
        options: [
          { id: "a", text: "The model performs well on training data but poorly on new data" },
          { id: "b", text: "The model trains too slowly" },
          { id: "c", text: "The dataset is too small to load into memory" },
          { id: "d", text: "The model has too few parameters" },
        ],
        correctOptionId: "a",
      },
      {
        id: "q4",
        prompt: "Which technique helps reduce overfitting?",
        options: [
          { id: "a", text: "Removing all validation data" },
          { id: "b", text: "Increasing model complexity indefinitely" },
          { id: "c", text: "Regularization" },
          { id: "d", text: "Training only on the test set" },
        ],
        correctOptionId: "c",
      },
      {
        id: "q5",
        prompt: "In scikit-learn, which method is typically used to fit a model to training data?",
        options: [
          { id: "a", text: ".predict()" },
          { id: "b", text: ".fit()" },
          { id: "c", text: ".transform()" },
          { id: "d", text: ".score_only()" },
        ],
        correctOptionId: "b",
      },
    ],
  },
  n5: {
    id: "n5",
    title: "ML Fundamentals Checkpoint",
    skillsTested: ["Machine Learning"],
    passingScorePercent: 70,
    questions: [
      {
        id: "q1",
        prompt: "What is the main difference between supervised and unsupervised learning?",
        options: [
          { id: "a", text: "Supervised learning uses labeled data; unsupervised does not" },
          { id: "b", text: "Supervised learning is always faster to train" },
          { id: "c", text: "Unsupervised learning requires a GPU" },
          { id: "d", text: "There is no meaningful difference" },
        ],
        correctOptionId: "a",
      },
      {
        id: "q2",
        prompt: "Which metric is most appropriate for evaluating a classifier on an imbalanced dataset?",
        options: [
          { id: "a", text: "Raw accuracy" },
          { id: "b", text: "F1 score" },
          { id: "c", text: "Mean squared error" },
          { id: "d", text: "R-squared" },
        ],
        correctOptionId: "b",
      },
      {
        id: "q3",
        prompt: "What does 'overfitting' mean?",
        options: [
          { id: "a", text: "The model performs well on training data but poorly on new data" },
          { id: "b", text: "The model trains too slowly" },
          { id: "c", text: "The dataset is too small to load into memory" },
          { id: "d", text: "The model has too few parameters" },
        ],
        correctOptionId: "a",
      },
      {
        id: "q4",
        prompt: "Which technique helps reduce overfitting?",
        options: [
          { id: "a", text: "Removing all validation data" },
          { id: "b", text: "Increasing model complexity indefinitely" },
          { id: "c", text: "Regularization" },
          { id: "d", text: "Training only on the test set" },
        ],
        correctOptionId: "c",
      },
      {
        id: "q5",
        prompt: "In scikit-learn, which method is typically used to fit a model to training data?",
        options: [
          { id: "a", text: ".predict()" },
          { id: "b", text: ".fit()" },
          { id: "c", text: ".transform()" },
          { id: "d", text: ".score_only()" },
        ],
        correctOptionId: "b",
      },
    ],
  },
};

// The full catalog — independent of personalized scoring. Includes courses
// r1-r5 (so links from Recommendations resolve to the same items) plus a
// broader set spanning all five careers, so /courses has something to browse
// beyond what's been pushed to any one learner.
export const mockCourseCatalog: Course[] = [
  {
    id: "r1",
    title: "Statistics for Data Science",
    type: "course",
    difficulty: "Beginner",
    estimatedHours: 12,
    rating: 4.7,
    skillsCovered: ["Statistics"],
    description:
      "A practical statistics course covering distributions, hypothesis testing, and regression fundamentals used throughout data science workflows.",
  },
  {
    id: "r2",
    title: "Intro to Machine Learning",
    type: "course",
    difficulty: "Beginner",
    estimatedHours: 18,
    rating: 4.8,
    skillsCovered: ["Machine Learning"],
    description:
      "Covers supervised and unsupervised learning, model evaluation, and scikit-learn basics with applied notebooks.",
  },
  {
    id: "r3",
    title: "SQL Query Practice Set",
    type: "practice",
    difficulty: "Intermediate",
    estimatedHours: 4,
    rating: 4.5,
    skillsCovered: ["SQL"],
    description: "A set of 25 progressively harder SQL queries against a retail dataset, with instant feedback.",
  },
  {
    id: "r4",
    title: "Exploratory Data Analysis Project",
    type: "project",
    difficulty: "Intermediate",
    estimatedHours: 10,
    rating: 4.6,
    skillsCovered: ["Data Visualization", "Statistics"],
    description:
      "Analyze a real-world dataset end-to-end and present findings with charts and a short written summary.",
  },
  {
    id: "r5",
    title: "ML Fundamentals Checkpoint",
    type: "assessment",
    difficulty: "Beginner",
    estimatedHours: 1,
    rating: 4.3,
    skillsCovered: ["Machine Learning"],
    description: "A short quiz checking core ML vocabulary and concepts before you proceed.",
  },
  {
    id: "c1",
    title: "Python for Everybody",
    type: "course",
    difficulty: "Beginner",
    estimatedHours: 20,
    rating: 4.9,
    skillsCovered: ["Python"],
    description: "Ground-up introduction to Python syntax, data structures, and writing your first scripts.",
  },
  {
    id: "c2",
    title: "Deep Learning Foundations",
    type: "course",
    difficulty: "Advanced",
    estimatedHours: 24,
    rating: 4.7,
    skillsCovered: ["Machine Learning", "Python"],
    description: "Neural network fundamentals, backpropagation, and building models with PyTorch.",
  },
  {
    id: "c3",
    title: "React & TypeScript Bootcamp",
    type: "course",
    difficulty: "Intermediate",
    estimatedHours: 22,
    rating: 4.6,
    skillsCovered: ["JavaScript", "React"],
    description: "Build production-grade UIs with React, TypeScript, hooks, and component design patterns.",
  },
  {
    id: "c4",
    title: "REST API Design with Node.js",
    type: "course",
    difficulty: "Intermediate",
    estimatedHours: 14,
    rating: 4.4,
    skillsCovered: ["Node.js", "API Design"],
    description: "Design and build RESTful APIs, covering auth, validation, and error handling patterns.",
  },
  {
    id: "c5",
    title: "Data Cleaning Practice Set",
    type: "practice",
    difficulty: "Beginner",
    estimatedHours: 6,
    rating: 4.2,
    skillsCovered: ["Python", "SQL"],
    description: "Hands-on exercises cleaning messy, real-world datasets before they're ready for analysis.",
  },
  {
    id: "c6",
    title: "Full Stack Capstone: Task Tracker",
    type: "project",
    difficulty: "Advanced",
    estimatedHours: 30,
    rating: 4.8,
    skillsCovered: ["React", "Node.js", "SQL"],
    description: "Build and deploy a complete task-tracking app with a React frontend and a Node/SQL backend.",
  },
  {
    id: "c7",
    title: "A/B Testing & Experiment Design",
    type: "course",
    difficulty: "Intermediate",
    estimatedHours: 9,
    rating: 4.5,
    skillsCovered: ["Statistics"],
    description: "How to design, run, and interpret A/B tests without fooling yourself with the results.",
  },
  {
    id: "c8",
    title: "Data Visualization with D3",
    type: "course",
    difficulty: "Intermediate",
    estimatedHours: 16,
    rating: 4.3,
    skillsCovered: ["Data Visualization", "JavaScript"],
    description: "Build custom, interactive charts and dashboards using D3.js from first principles.",
  },
  {
    id: "c9",
    title: "MLOps Fundamentals Checkpoint",
    type: "assessment",
    difficulty: "Advanced",
    estimatedHours: 1,
    rating: 4.1,
    skillsCovered: ["Machine Learning"],
    description: "Checks understanding of model deployment, monitoring, and versioning concepts.",
  },
  {
    id: "c10",
    title: "SQL for Analysts",
    type: "course",
    difficulty: "Beginner",
    estimatedHours: 11,
    rating: 4.6,
    skillsCovered: ["SQL"],
    description: "From SELECT statements to window functions — the SQL an analyst uses daily.",
  },
];

// Activity log — computed relative to "now" so the demo always looks current.
function daysAgo(n: number, hour = 14): string {
  const d = new Date();
  d.setDate(d.getDate() - n);
  d.setHours(hour, 30, 0, 0);
  return d.toISOString();
}

export const mockActivityLog: ActivityEvent[] = (
  [
    {
      id: "a1",
      type: "resource_completed",
      title: "Python Refresher",
      detail: "Course · 6 hrs",
      timestamp: daysAgo(21, 10),
    },
    {
      id: "a2",
      type: "feedback_given",
      title: "Python Refresher",
      detail: "Appropriate",
      timestamp: daysAgo(21, 11),
    },
    {
      id: "a3",
      type: "assessment_taken",
      title: "Python Basics Checkpoint",
      detail: "Passed · 90%",
      timestamp: daysAgo(20, 9),
    },
    {
      id: "a4",
      type: "resource_completed",
      title: "SQL Query Practice Set",
      detail: "Practice · 4 hrs",
      timestamp: daysAgo(14, 16),
    },
    {
      id: "a5",
      type: "feedback_given",
      title: "SQL Query Practice Set",
      detail: "Too easy",
      timestamp: daysAgo(14, 16),
    },
    {
      id: "a6",
      type: "resource_completed",
      title: "Statistics for Data Science — Module 1",
      detail: "Course · 3 hrs",
      timestamp: daysAgo(9, 19),
    },
    {
      id: "a7",
      type: "assessment_taken",
      title: "Statistics Basics Quiz",
      detail: "Not passed · 55%",
      timestamp: daysAgo(8, 12),
    },
    {
      id: "a8",
      type: "feedback_given",
      title: "Statistics Basics Quiz",
      detail: "Too difficult",
      timestamp: daysAgo(8, 12),
    },
    {
      id: "a9",
      type: "assessment_taken",
      title: "Statistics Basics Quiz",
      detail: "Passed · 80%",
      timestamp: daysAgo(6, 17),
    },
    {
      id: "a10",
      type: "resource_completed",
      title: "Statistics for Data Science",
      detail: "Course · 12 hrs",
      timestamp: daysAgo(6, 17),
    },
    {
      id: "a11",
      type: "feedback_given",
      title: "Statistics for Data Science",
      detail: "Appropriate",
      timestamp: daysAgo(6, 18),
    },
    {
      id: "a12",
      type: "resource_completed",
      title: "Exploratory Data Analysis Project — Draft",
      detail: "Project · 4 hrs logged",
      timestamp: daysAgo(1, 20),
    },
  ] as ActivityEvent[]
).sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

// Career catalog — mirrors the `careers` + `career_skills` tables.
export const mockCareerCatalog: CareerProfile[] = [
  {
    id: "Data Scientist",
    title: "Data Scientist",
    tagline: "Turn raw data into decisions",
    description:
      "Analyzes structured and unstructured data to find patterns, build predictive models, and communicate findings that guide business decisions.",
    typicalTimeframe: "6–9 months from beginner",
    requiredSkills: [
      { skillName: "Python", level: 5, core: true },
      { skillName: "Statistics", level: 4, core: true },
      { skillName: "SQL", level: 4, core: true },
      { skillName: "Machine Learning", level: 4, core: true },
      { skillName: "Data Visualization", level: 3, core: false },
    ],
  },
  {
    id: "AI Engineer",
    title: "AI Engineer",
    tagline: "Build and ship intelligent systems",
    description:
      "Designs, trains, and deploys machine learning and generative AI models into production applications, with a strong focus on engineering and scalability.",
    typicalTimeframe: "8–12 months from beginner",
    requiredSkills: [
      { skillName: "Python", level: 5, core: true },
      { skillName: "Machine Learning", level: 5, core: true },
      { skillName: "Deep Learning", level: 4, core: true },
      { skillName: "Statistics", level: 3, core: false },
      { skillName: "SQL", level: 3, core: false },
    ],
  },
  {
    id: "Machine Learning Engineer",
    title: "Machine Learning Engineer",
    tagline: "Take models from notebook to production",
    description:
      "Bridges data science and software engineering — builds the pipelines, infrastructure, and monitoring that keep ML models reliable at scale.",
    typicalTimeframe: "7–10 months from beginner",
    requiredSkills: [
      { skillName: "Python", level: 5, core: true },
      { skillName: "Machine Learning", level: 5, core: true },
      { skillName: "SQL", level: 3, core: false },
      { skillName: "Statistics", level: 3, core: false },
      { skillName: "Node.js", level: 2, core: false },
    ],
  },
  {
    id: "Data Analyst",
    title: "Data Analyst",
    tagline: "Answer business questions with data",
    description:
      "Explores datasets, builds dashboards, and runs analyses that help teams understand what happened and why — the most common entry point into data work.",
    typicalTimeframe: "3–5 months from beginner",
    requiredSkills: [
      { skillName: "SQL", level: 4, core: true },
      { skillName: "Data Visualization", level: 4, core: true },
      { skillName: "Statistics", level: 3, core: true },
      { skillName: "Python", level: 2, core: false },
    ],
  },
  {
    id: "Full Stack Developer",
    title: "Full Stack Developer",
    tagline: "Build the whole product, front to back",
    description:
      "Builds complete web applications — from database schema and API design to the interfaces users actually interact with.",
    typicalTimeframe: "5–8 months from beginner",
    requiredSkills: [
      { skillName: "JavaScript", level: 4, core: true },
      { skillName: "React", level: 4, core: true },
      { skillName: "Node.js", level: 4, core: true },
      { skillName: "SQL", level: 3, core: false },
      { skillName: "API Design", level: 3, core: false },
    ],
  },
];

// Notifications — ties the backend's adaptive-repair logic (recommendation
// re-scoring after feedback, roadmap unlocks after prerequisites complete)
// to something visible in the UI.
export const mockNotifications: NotificationItem[] = (
  [
    {
      id: "notif1",
      type: "milestone_unlocked",
      title: "New step unlocked",
      body: "\"Intro to Machine Learning\" is now available — you finished its prerequisite.",
      timestamp: daysAgo(0, 9),
      read: false,
      linkTo: "/roadmap",
    },
    {
      id: "notif2",
      type: "path_adjusted",
      title: "Your path was adjusted",
      body: "Based on your \"too difficult\" feedback, we added a review step before the next assessment.",
      timestamp: daysAgo(1, 18),
      read: false,
      linkTo: "/roadmap",
    },
    {
      id: "notif3",
      type: "new_recommendation",
      title: "New recommendation",
      body: "\"Exploratory Data Analysis Project\" was added — it fits two skills you're building.",
      timestamp: daysAgo(3, 11),
      read: true,
      linkTo: "/recommendations",
    },
    {
      id: "notif4",
      type: "milestone_unlocked",
      title: "New step unlocked",
      body: "\"SQL Query Practice Set\" is now available.",
      timestamp: daysAgo(6, 17),
      read: true,
      linkTo: "/roadmap",
    },
    {
      id: "notif5",
      type: "path_adjusted",
      title: "Your path was adjusted",
      body: "Statistics for Data Science moved earlier — it's a prerequisite for two upcoming steps.",
      timestamp: daysAgo(9, 8),
      read: true,
      linkTo: "/roadmap",
    },
  ] as NotificationItem[]
).sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

// Achievements & streaks — lightweight gamification layered over progress
// data that already exists (completions, assessments, feedback).
export const mockAchievements: Achievement[] = [
  {
    id: "ach1",
    title: "First Step",
    description: "Complete your first course.",
    icon: "🎯",
    earned: true,
    earnedAt: daysAgo(21, 10),
  },
  {
    id: "ach2",
    title: "Quiz Whiz",
    description: "Pass your first assessment.",
    icon: "🧠",
    earned: true,
    earnedAt: daysAgo(20, 9),
  },
  {
    id: "ach3",
    title: "Feedback Friend",
    description: "Give feedback on 3 resources.",
    icon: "💬",
    earned: true,
    earnedAt: daysAgo(8, 12),
  },
  {
    id: "ach4",
    title: "Week One",
    description: "Stay active for 7 days in a row.",
    icon: "🔥",
    earned: false,
  },
  {
    id: "ach5",
    title: "Halfway There",
    description: "Reach 50% overall roadmap completion.",
    icon: "🏔️",
    earned: false,
  },
  {
    id: "ach6",
    title: "Project Builder",
    description: "Complete your first project.",
    icon: "🛠️",
    earned: false,
  },
  {
    id: "ach7",
    title: "Skill Stacker",
    description: "Reach proficiency 4+ in three skills.",
    icon: "📈",
    earned: false,
  },
  {
    id: "ach8",
    title: "Path Complete",
    description: "Finish your entire learning roadmap.",
    icon: "🏁",
    earned: false,
  },
];

export const mockStreak: StreakInfo = {
  currentStreak: 4,
  longestStreak: 9,
  lastActiveDate: daysAgo(0),
  // Mon..Sun for the current week — true where the learner was active
  activeDaysThisWeek: [true, true, false, true, true, false, false],
};
