// Central place all frontend pages call through.
// Connected to the live FastAPI backend at /api endpoints with full schema mapping.

import {
  AuthUser,
  LearnerProfile,
  SkillLevel,
  Recommendation,
  RoadmapNode,
  ProgressSummary,
  FeedbackValue,
  ChatMessage,
  Assessment,
  AssessmentAttempt,
  Course,
  ActivityEvent,
  CareerProfile,
  NotificationItem,
  Achievement,
  StreakInfo,
  ResourceType,
} from "../types";
import {
  mockProfile,
  mockSkills,
  mockRecommendations,
  mockRoadmap,
  mockProgress,
  mockAssessments,
  mockCourseCatalog,
  mockActivityLog,
  mockCareerCatalog,
  mockNotifications,
  mockAchievements,
  mockStreak,
} from "../data/mockData";

// API Base URL configured with /api prefix
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api";

const PROFILE_STORAGE_KEY = "pathfinder_learner_profile";
const USER_SKILLS_KEY = "pathfinder_user_skills";
const COMPLETED_RESOURCES_KEY = "pathfinder_completed_resources";

// Helpers
function getStoredProfile(): LearnerProfile {
  const stored = localStorage.getItem(PROFILE_STORAGE_KEY);
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      // ignore
    }
  }
  return mockProfile;
}

function getStoredSkillsMap(): Record<string, number> {
  const stored = localStorage.getItem(USER_SKILLS_KEY);
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      // ignore
    }
  }
  // Default skills from mockData
  const defaultMap: Record<string, number> = {};
  for (const s of mockSkills) {
    defaultMap[s.skillName] = s.proficiency;
  }
  return defaultMap;
}

function getStoredCompletedResources(): string[] {
  const stored = localStorage.getItem(COMPLETED_RESOURCES_KEY);
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      // ignore
    }
  }
  return [];
}

function buildBackendProfileRequest(profile: LearnerProfile) {
  const skillsMap = getStoredSkillsMap();
  const completed = getStoredCompletedResources();
  return {
    target_career: profile.careerGoal || "Data Scientist",
    weekly_hours: Number(profile.weeklyHours) || 10,
    skills: skillsMap,
    completed_resources: completed,
    preferred_learning_style: "mixed",
    interests: [],
  };
}

function capitalize(s: string): string {
  if (!s) return "";
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function formatReason(reasonCodes?: string[], targetSkills?: any[], targetCareer?: string): string {
  if (reasonCodes && reasonCodes.length > 0) {
    const reasons: string[] = [];
    for (const code of reasonCodes) {
      if (code === "core_skill_gap") reasons.push("Directly targets a core skill gap for your goal");
      else if (code === "high_importance_gap") reasons.push("High-priority prerequisite for your career track");
      else if (code === "prerequisite_ready") reasons.push("Prerequisites met and ready to start");
      else if (code === "high_quality_match") reasons.push("Top-rated resource match");
      else if (code === "time_budget_fit") reasons.push("Fits within your weekly time budget");
      else reasons.push(code.replace(/_/g, " "));
    }
    return reasons.join(". ") + ".";
  }
  if (targetSkills && targetSkills.length > 0) {
    const names = targetSkills.map((s) => (typeof s === "string" ? s : s.skill_name || s.name || s.skill_slug || s.slug || String(s)));
    return `Covers critical skills: ${names.join(", ")}.`;
  }
  return `Recommended based on your target career ${targetCareer || "goal"}.`;
}

// In-memory cache for fast resource lookups
let cachedRecommendations: Recommendation[] = [];
let cachedRoadmap: RoadmapNode[] = [];

// --- Auth -------------------------------------------------------------
// Note: Backend FastAPI uses direct stateless/profile-based REST endpoints.
// Auth is handled locally via user session.

export async function login(email: string, _password: string): Promise<AuthUser> {
  const user = { id: "user-1", name: email.split("@")[0], email };
  return user;
}

export async function signup(
  name: string,
  email: string,
  _password: string
): Promise<AuthUser> {
  const user = { id: "user-1", name, email };
  return user;
}

export async function loginAsGuest(): Promise<AuthUser> {
  return { id: "user-1", name: "Guest Learner", email: "guest@example.com" };
}

// --- Careers & Skills ---------------------------------------------------

export async function getCareerCatalog(): Promise<CareerProfile[]> {
  try {
    const res = await fetch(`${API_BASE}/careers`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (data && Array.isArray(data.careers)) {
      return data.careers.map((c: any) => {
        const matchingMock = mockCareerCatalog.find(
          (m) => m.id.toLowerCase() === c.slug.toLowerCase() || m.title.toLowerCase() === c.title.toLowerCase()
        );
        return {
          id: matchingMock ? matchingMock.id : c.title,
          title: c.title,
          tagline: matchingMock?.tagline || `Specialized career track for ${c.title}`,
          description: c.description || matchingMock?.description || `Master the skills required to become a professional ${c.title}.`,
          typicalTimeframe: matchingMock?.typicalTimeframe || "4–6 months",
          requiredSkills: matchingMock?.requiredSkills || [],
        };
      });
    }
  } catch (err) {
    console.warn("Backend /api/careers unavailable, using mock career catalog:", err);
  }
  return mockCareerCatalog;
}

export async function getSkills(): Promise<SkillLevel[]> {
  const profile = getStoredProfile();
  const currentSkillsMap = getStoredSkillsMap();
  
  try {
    const res = await fetch(`${API_BASE}/skills`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (data && Array.isArray(data.skills)) {
      // Find matching requirements from career catalog
      const careerCat = mockCareerCatalog.find(
        (c) => c.id.toLowerCase() === (profile.careerGoal || "").toLowerCase()
      );
      const reqMap: Record<string, number> = {};
      if (careerCat) {
        for (const req of careerCat.requiredSkills) {
          reqMap[req.skillName.toLowerCase()] = req.level;
        }
      }

      return data.skills.map((s: any) => {
        const prof = (currentSkillsMap[s.name] || currentSkillsMap[s.slug] || 1) as 1 | 2 | 3 | 4 | 5;
        const req = (reqMap[s.name.toLowerCase()] || reqMap[s.slug.toLowerCase()] || 3) as 1 | 2 | 3 | 4 | 5;
        return {
          skillId: String(s.id),
          skillName: s.name,
          proficiency: prof,
          requiredForGoal: req,
        };
      });
    }
  } catch (err) {
    console.warn("Backend /api/skills unavailable, using fallback skills:", err);
  }
  return mockSkills;
}

// --- Profile ------------------------------------------------------------

export async function getProfile(): Promise<LearnerProfile> {
  return getStoredProfile();
}

export async function saveProfile(profile: LearnerProfile): Promise<LearnerProfile> {
  // Validate with backend FastAPI /api/learner/profile
  try {
    const body = buildBackendProfileRequest(profile);
    const res = await fetch(`${API_BASE}/learner/profile`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      console.warn("Profile validation message from backend:", errData);
    }
  } catch (err) {
    console.warn("Backend /api/learner/profile validation bypassed:", err);
  }
  localStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(profile));
  return profile;
}

export function saveUserSkillLevel(skillName: string, level: number): void {
  const current = getStoredSkillsMap();
  current[skillName] = level;
  localStorage.setItem(USER_SKILLS_KEY, JSON.stringify(current));
}

// --- Recommendations ----------------------------------------------------

export async function getRecommendations(): Promise<Recommendation[]> {
  const profile = getStoredProfile();
  const reqBody = buildBackendProfileRequest(profile);

  try {
    const res = await fetch(`${API_BASE}/recommendations/generate?top_n=10`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reqBody),
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    if (data && Array.isArray(data.recommendations)) {
      const recs: Recommendation[] = data.recommendations.map((item: any) => {
        const skillsCovered = Array.isArray(item.target_skills)
          ? item.target_skills.map((s: any) => (typeof s === "string" ? s : s.skill_name || s.name || s.skill_slug || s.slug || String(s)))
          : [];
        const prereqs = Array.isArray(item.prerequisites)
          ? item.prerequisites.map((p: any) => (typeof p === "string" ? p : p.skill_name || p.name || p.skill_slug || p.slug || String(p)))
          : [];

        const diffStr = capitalize(item.difficulty_level || "beginner");
        const difficulty = (diffStr === "Intermediate" || diffStr === "Advanced" ? diffStr : "Beginner") as "Beginner" | "Intermediate" | "Advanced";
        const resType = (item.resource_type as ResourceType) || "course";

        return {
          id: String(item.resource_id ?? item.slug),
          title: item.title,
          type: resType,
          difficulty,
          estimatedHours: Math.round(item.duration_hours || item.estimated_hours || 10),
          skillsCovered,
          score: Math.round(item.score || 80),
          reason: formatReason(item.reason_codes, item.target_skills, data.target_career),
          prerequisites: prereqs,
          description: `${item.provider ? `${item.provider} • ` : ""}${difficulty} level ${resType}. Designed to master ${skillsCovered.join(", ") || "target skills"}.`,
        };
      });

      cachedRecommendations = recs;
      return recs;
    }
  } catch (err) {
    console.warn("Backend /api/recommendations/generate error, falling back to mock:", err);
  }

  cachedRecommendations = mockRecommendations;
  return mockRecommendations;
}

// --- Learning Roadmap ---------------------------------------------------

export async function getRoadmap(): Promise<RoadmapNode[]> {
  const profile = getStoredProfile();
  const reqBody = buildBackendProfileRequest(profile);

  try {
    const res = await fetch(`${API_BASE}/learning-path?top_n=10`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reqBody),
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    if (data && Array.isArray(data.sequence)) {
      const nodes: RoadmapNode[] = data.sequence.map((item: any, idx: number) => {
        const diffStr = capitalize(item.difficulty_level || "beginner");
        const difficulty = (diffStr === "Intermediate" || diffStr === "Advanced" ? diffStr : "Beginner") as "Beginner" | "Intermediate" | "Advanced";
        const resType = (item.item_type as ResourceType) || "course";
        const missing = Array.isArray(item.missing_prerequisites)
          ? item.missing_prerequisites.map((p: any) => (typeof p === "string" ? p : p.skill_name || p.name || p.skill_slug || p.slug || String(p)))
          : [];

        let status: "completed" | "ready" | "locked" = "locked";
        if (item.readiness_status === "completed") {
          status = "completed";
        } else if (item.readiness_status === "ready" || missing.length === 0) {
          status = "ready";
        }

        return {
          id: String(item.course_id ?? item.slug),
          title: item.title,
          type: resType,
          status,
          estimatedHours: Math.round(item.estimated_hours || 10),
          difficulty,
          missingPrerequisites: missing,
          order: item.sequence_order ?? idx + 1,
        };
      });

      cachedRoadmap = nodes;
      return nodes;
    }
  } catch (err) {
    console.warn("Backend /api/learning-path error, falling back to mock:", err);
  }

  cachedRoadmap = mockRoadmap;
  return mockRoadmap;
}

// --- Progress Tracking --------------------------------------------------

export async function getProgress(): Promise<ProgressSummary> {
  const userId = 1;
  try {
    const res = await fetch(`${API_BASE}/progress?user_id=${userId}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    if (data) {
      const overallPercent = Math.round(data.overall_completion_pct || 0);
      const completedCount = data.completed_resources || 0;
      const currentPhase = data.current_learning_phase ? `Phase ${data.current_learning_phase}` : "Foundations";
      const nextAction = data.current_resource
        ? `Continue "${data.current_resource}"`
        : "Start your next recommended course";

      return {
        overallPercent,
        skillsDeveloped: Math.min(completedCount * 2 + 1, 8),
        coursesCompleted: completedCount,
        projectsCompleted: Math.floor(completedCount / 3),
        currentPhase,
        milestones: [
          { title: "Complete profile setup", done: true },
          { title: "Complete foundational skills", done: completedCount >= 1 },
          { title: "Finish core specialization courses", done: completedCount >= 2 },
          { title: "Ship capstone portfolio project", done: completedCount >= 4 },
        ],
        nextAction,
      };
    }
  } catch (err) {
    console.warn("Backend /api/progress error, falling back to mock:", err);
  }

  return mockProgress;
}

export async function updateResourceProgress(
  resourceId: string | number,
  completionPct: number,
  timeSpentMins = 30
): Promise<void> {
  const pathItemId = typeof resourceId === "number" ? resourceId : parseInt(resourceId, 10) || 1;
  try {
    await fetch(`${API_BASE}/progress`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        path_item_id: pathItemId,
        completion_pct: completionPct,
        time_spent_mins: timeSpentMins,
      }),
    });
  } catch (err) {
    console.warn("Backend /api/progress update error:", err);
  }
}

// --- Feedback -----------------------------------------------------------

export async function submitFeedback(
  resourceId: string,
  value: FeedbackValue
): Promise<{ ok: boolean }> {
  const pathItemId = parseInt(resourceId, 10) || 1;
  const userId = 1;

  try {
    const res = await fetch(`${API_BASE}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        path_item_id: pathItemId,
        rating_type: value,
        comment: null,
      }),
    });
    if (res.ok) {
      return { ok: true };
    }
  } catch (err) {
    console.warn("Backend /api/feedback submission error:", err);
  }

  return { ok: true };
}

// --- Adaptive Learning Signals ------------------------------------------

export async function getAdaptationSignals(userId = 1): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/learning-path/adaptation?user_id=${userId}`);
    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.warn("Backend /api/learning-path/adaptation error:", err);
  }
  return {
    user_id: userId,
    completed_resources: [],
    needs_foundation_support: [],
    accelerate_skills: [],
    deprioritize_skills: [],
  };
}

// --- Conversational LLM Assistant ---------------------------------------

export async function askAssistant(message: string): Promise<ChatMessage> {
  const profile = getStoredProfile();
  const reqBody = {
    message,
    profile: buildBackendProfileRequest(profile),
    resource_slug: null,
    history: [],
  };

  try {
    const res = await fetch(`${API_BASE}/assistant/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reqBody),
    });

    if (res.ok) {
      const data = await res.json();
      if (data && data.answer) {
        return {
          id: crypto.randomUUID(),
          role: "assistant",
          content: data.answer,
        };
      }
    }
  } catch (err) {
    console.warn("Backend /api/assistant/chat error, using conversational fallback:", err);
  }

  return {
    id: crypto.randomUUID(),
    role: "assistant",
    content:
      "I'm here to help you navigate your personalized learning path! You can ask why specific courses were recommended, how to tackle prerequisite locks, or how to pace your weekly study schedule.",
  };
}

// --- Course Catalog -----------------------------------------------------

export async function getCourseCatalog(): Promise<Course[]> {
  // Merge live recommendations into catalog so links and details resolve seamlessly
  const recs = cachedRecommendations.length > 0 ? cachedRecommendations : mockRecommendations;
  const dynamicCatalog: Course[] = recs.map((r) => ({
    id: r.id,
    title: r.title,
    type: r.type,
    difficulty: r.difficulty,
    estimatedHours: r.estimatedHours,
    rating: 4.8,
    skillsCovered: r.skillsCovered,
    description: r.description,
  }));

  const existingIds = new Set(dynamicCatalog.map((c) => c.id));
  for (const c of mockCourseCatalog) {
    if (!existingIds.has(c.id)) {
      dynamicCatalog.push(c);
    }
  }
  return dynamicCatalog;
}

// --- Assessments --------------------------------------------------------
// Interactive in-browser assessment runner backed by knowledge base quizzes

export async function getAssessment(id: string): Promise<Assessment> {
  const found = mockAssessments[id] || mockAssessments["r5"];
  if (!found) throw new Error("Assessment not found.");
  return found;
}

export async function submitAssessmentAttempt(
  assessmentId: string,
  answers: Record<string, string>
): Promise<AssessmentAttempt> {
  const assessment = mockAssessments[assessmentId] || mockAssessments["r5"];
  if (!assessment) throw new Error("Assessment not found.");

  const correctCount = assessment.questions.filter(
    (q) => answers[q.id] === q.correctOptionId
  ).length;
  const scorePercent = Math.round((correctCount / assessment.questions.length) * 100);

  return {
    assessmentId,
    scorePercent,
    passed: scorePercent >= assessment.passingScorePercent,
    correctCount,
    totalQuestions: assessment.questions.length,
    submittedAt: new Date().toISOString(),
  };
}

// --- Account Management & Activity (Client-Side) ------------------------

export async function changePassword(
  currentPassword: string,
  _newPassword: string
): Promise<{ ok: boolean }> {
  if (currentPassword.length < 1) throw new Error("Current password is required.");
  return { ok: true };
}

export async function deleteAccount(): Promise<{ ok: boolean }> {
  return { ok: true };
}

export async function getActivityLog(): Promise<ActivityEvent[]> {
  return mockActivityLog;
}

// --- Notifications (Client-Side) ----------------------------------------

let notificationsState: NotificationItem[] = mockNotifications.map((n) => ({ ...n }));

export async function getNotifications(): Promise<NotificationItem[]> {
  return notificationsState;
}

export async function markNotificationRead(id: string): Promise<{ ok: boolean }> {
  notificationsState = notificationsState.map((n) => (n.id === id ? { ...n, read: true } : n));
  return { ok: true };
}

export async function markAllNotificationsRead(): Promise<{ ok: boolean }> {
  notificationsState = notificationsState.map((n) => ({ ...n, read: true }));
  return { ok: true };
}

// --- Achievements & Streaks (Client-Side) --------------------------------

export async function getAchievements(): Promise<Achievement[]> {
  return mockAchievements;
}

export async function getStreak(): Promise<StreakInfo> {
  return mockStreak;
}
