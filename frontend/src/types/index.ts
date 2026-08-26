// Shared domain types — kept in sync with the backend's SQLAlchemy models.
// Frontend NEVER computes scores/gaps/roadmaps itself; it only renders what
// the backend (or, for now, mock data) provides.

export type CareerGoal =
  | "Data Scientist"
  | "AI Engineer"
  | "Machine Learning Engineer"
  | "Data Analyst"
  | "Full Stack Developer";

export interface AuthUser {
  id: string;
  name: string;
  email: string;
}

export interface LearnerProfile {
  id: string;
  name: string;
  careerGoal: CareerGoal;
  weeklyHours: number;
  experienceLevel: "Beginner" | "Intermediate" | "Advanced";
  preferences?: string;
}

export interface SkillLevel {
  skillId: string;
  skillName: string;
  proficiency: 1 | 2 | 3 | 4 | 5;
  requiredForGoal?: 1 | 2 | 3 | 4 | 5;
}

export type ResourceType = "course" | "project" | "practice" | "assessment";

export interface Recommendation {
  id: string;
  title: string;
  type: ResourceType;
  difficulty: "Beginner" | "Intermediate" | "Advanced";
  estimatedHours: number;
  skillsCovered: string[];
  score: number; // 0-100, provided by backend scoring engine
  reason: string; // LLM-generated explanation
  prerequisites: string[]; // skill or resource names
  description: string;
}

export type RoadmapStatus = "completed" | "ready" | "locked";

export interface RoadmapNode {
  id: string;
  title: string;
  type: ResourceType;
  status: RoadmapStatus;
  estimatedHours: number;
  difficulty: "Beginner" | "Intermediate" | "Advanced";
  missingPrerequisites: string[];
  order: number;
}

export interface ProgressSummary {
  overallPercent: number;
  skillsDeveloped: number;
  coursesCompleted: number;
  projectsCompleted: number;
  currentPhase: string;
  milestones: { title: string; done: boolean }[];
  nextAction: string;
}

export interface AssessmentQuestion {
  id: string;
  prompt: string;
  options: { id: string; text: string }[];
  correctOptionId: string;
}

export interface Assessment {
  id: string;
  title: string;
  skillsTested: string[];
  passingScorePercent: number;
  questions: AssessmentQuestion[];
}

export interface AssessmentAttempt {
  assessmentId: string;
  scorePercent: number;
  passed: boolean;
  correctCount: number;
  totalQuestions: number;
  submittedAt: string;
}

export interface Course {
  id: string;
  title: string;
  type: ResourceType;
  difficulty: "Beginner" | "Intermediate" | "Advanced";
  estimatedHours: number;
  rating: number; // 0-5
  skillsCovered: string[];
  description: string;
}

export type ActivityEventType = "resource_completed" | "feedback_given" | "assessment_taken";

export interface ActivityEvent {
  id: string;
  type: ActivityEventType;
  title: string;
  detail?: string;
  timestamp: string; // ISO 8601
}

export interface CareerSkillRequirement {
  skillName: string;
  level: 1 | 2 | 3 | 4 | 5;
  core: boolean;
}

export interface CareerProfile {
  id: CareerGoal;
  title: CareerGoal;
  tagline: string;
  description: string;
  typicalTimeframe: string;
  requiredSkills: CareerSkillRequirement[];
}

export type NotificationType = "new_recommendation" | "milestone_unlocked" | "path_adjusted";

export interface NotificationItem {
  id: string;
  type: NotificationType;
  title: string;
  body: string;
  timestamp: string; // ISO 8601
  read: boolean;
  linkTo?: string;
}

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  earned: boolean;
  earnedAt?: string;
}

export interface StreakInfo {
  currentStreak: number;
  longestStreak: number;
  lastActiveDate: string; // ISO date
  activeDaysThisWeek: boolean[]; // Mon..Sun
}

export type FeedbackValue = "too_easy" | "appropriate" | "too_difficult" | "not_relevant";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
}
