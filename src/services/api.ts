// Central place all pages call through. Today every function resolves
// mock data with a small artificial delay so loading states are visible.
// When FastAPI is ready: set USE_MOCK = false and fill in the fetch calls —
// no page component needs to change.

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

const USE_MOCK = true;
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";
const MOCK_DELAY_MS = 400;

function delay<T>(value: T): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(value), MOCK_DELAY_MS));
}

// --- Auth -------------------------------------------------------------
// Mock implementation "authenticates" anyone and stores a fake user object.
// Swap for real calls to a FastAPI /auth/login and /auth/signup once the
// backend has session/JWT handling — the function signatures won't change.

export async function login(email: string, _password: string): Promise<AuthUser> {
  if (USE_MOCK) {
    return delay({ id: "user-1", name: email.split("@")[0], email });
  }
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password: _password }),
  });
  if (!res.ok) throw new Error("Invalid email or password.");
  return res.json();
}

export async function signup(
  name: string,
  email: string,
  _password: string
): Promise<AuthUser> {
  if (USE_MOCK) {
    return delay({ id: crypto.randomUUID(), name, email });
  }
  const res = await fetch(`${API_BASE}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password: _password }),
  });
  if (!res.ok) throw new Error("Could not create account.");
  return res.json();
}

export async function loginAsGuest(): Promise<AuthUser> {
  return delay({ id: "guest", name: "Guest", email: "guest@example.com" });
}

// --- Profile ------------------------------------------------------------

export async function getProfile(): Promise<LearnerProfile> {
  if (USE_MOCK) return delay(mockProfile);
  const res = await fetch(`${API_BASE}/profile`);
  return res.json();
}

export async function saveProfile(profile: LearnerProfile): Promise<LearnerProfile> {
  if (USE_MOCK) return delay(profile);
  const res = await fetch(`${API_BASE}/profile`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  return res.json();
}

export async function getSkills(): Promise<SkillLevel[]> {
  if (USE_MOCK) return delay(mockSkills);
  const res = await fetch(`${API_BASE}/skills`);
  return res.json();
}

export async function getRecommendations(): Promise<Recommendation[]> {
  if (USE_MOCK) return delay(mockRecommendations);
  const res = await fetch(`${API_BASE}/recommendations`);
  return res.json();
}

export async function getRoadmap(): Promise<RoadmapNode[]> {
  if (USE_MOCK) return delay(mockRoadmap);
  const res = await fetch(`${API_BASE}/roadmap`);
  return res.json();
}

export async function getProgress(): Promise<ProgressSummary> {
  if (USE_MOCK) return delay(mockProgress);
  const res = await fetch(`${API_BASE}/progress`);
  return res.json();
}

export async function submitFeedback(
  resourceId: string,
  value: FeedbackValue
): Promise<{ ok: boolean }> {
  if (USE_MOCK) return delay({ ok: true });
  const res = await fetch(`${API_BASE}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ resourceId, value }),
  });
  return res.json();
}

export async function askAssistant(message: string): Promise<ChatMessage> {
  if (USE_MOCK) {
    return delay({
      id: crypto.randomUUID(),
      role: "assistant",
      content:
        "This is a mock response. Once the backend is connected, this will call the Gemini-powered assistant endpoint and answer based on your actual profile and roadmap.",
    });
  }
  const res = await fetch(`${API_BASE}/assistant`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  return res.json();
}

// --- Assessments ----------------------------------------------------------

export async function getAssessment(id: string): Promise<Assessment> {
  if (USE_MOCK) {
    const found = mockAssessments[id];
    if (!found) throw new Error("Assessment not found.");
    return delay(found);
  }
  const res = await fetch(`${API_BASE}/assessments/${id}`);
  if (!res.ok) throw new Error("Assessment not found.");
  return res.json();
}

export async function submitAssessmentAttempt(
  assessmentId: string,
  answers: Record<string, string>
): Promise<AssessmentAttempt> {
  if (USE_MOCK) {
    const assessment = mockAssessments[assessmentId];
    if (!assessment) throw new Error("Assessment not found.");
    const correctCount = assessment.questions.filter(
      (q) => answers[q.id] === q.correctOptionId
    ).length;
    const scorePercent = Math.round((correctCount / assessment.questions.length) * 100);
    return delay({
      assessmentId,
      scorePercent,
      passed: scorePercent >= assessment.passingScorePercent,
      correctCount,
      totalQuestions: assessment.questions.length,
      submittedAt: new Date().toISOString(),
    });
  }
  const res = await fetch(`${API_BASE}/assessment_results`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ assessmentId, answers }),
  });
  return res.json();
}

// --- Course Catalog ---------------------------------------------------

export async function getCourseCatalog(): Promise<Course[]> {
  if (USE_MOCK) return delay(mockCourseCatalog);
  const res = await fetch(`${API_BASE}/courses`);
  return res.json();
}

// --- Account management -------------------------------------------------

export async function changePassword(
  currentPassword: string,
  newPassword: string
): Promise<{ ok: boolean }> {
  if (USE_MOCK) {
    if (currentPassword.length < 1) throw new Error("Current password is required.");
    return delay({ ok: true });
  }
  const res = await fetch(`${API_BASE}/auth/change-password`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ currentPassword, newPassword }),
  });
  if (!res.ok) throw new Error("Could not update password.");
  return res.json();
}

export async function deleteAccount(): Promise<{ ok: boolean }> {
  if (USE_MOCK) return delay({ ok: true });
  const res = await fetch(`${API_BASE}/auth/account`, { method: "DELETE" });
  if (!res.ok) throw new Error("Could not delete account.");
  return res.json();
}

// --- Activity log ----------------------------------------------------

export async function getActivityLog(): Promise<ActivityEvent[]> {
  if (USE_MOCK) return delay(mockActivityLog);
  const res = await fetch(`${API_BASE}/activity`);
  return res.json();
}

// --- Career catalog ----------------------------------------------------

export async function getCareerCatalog(): Promise<CareerProfile[]> {
  if (USE_MOCK) return delay(mockCareerCatalog);
  const res = await fetch(`${API_BASE}/careers`);
  return res.json();
}

// --- Notifications --------------------------------------------------------
// In-memory mutable copy so "mark as read" persists for the session even
// though nothing is written to a real backend yet.
let notificationsState: NotificationItem[] = mockNotifications.map((n) => ({ ...n }));

export async function getNotifications(): Promise<NotificationItem[]> {
  if (USE_MOCK) return delay(notificationsState);
  const res = await fetch(`${API_BASE}/notifications`);
  return res.json();
}

export async function markNotificationRead(id: string): Promise<{ ok: boolean }> {
  if (USE_MOCK) {
    notificationsState = notificationsState.map((n) => (n.id === id ? { ...n, read: true } : n));
    return delay({ ok: true });
  }
  const res = await fetch(`${API_BASE}/notifications/${id}/read`, { method: "POST" });
  return res.json();
}

export async function markAllNotificationsRead(): Promise<{ ok: boolean }> {
  if (USE_MOCK) {
    notificationsState = notificationsState.map((n) => ({ ...n, read: true }));
    return delay({ ok: true });
  }
  const res = await fetch(`${API_BASE}/notifications/read-all`, { method: "POST" });
  return res.json();
}

// --- Achievements & streaks ------------------------------------------

export async function getAchievements(): Promise<Achievement[]> {
  if (USE_MOCK) return delay(mockAchievements);
  const res = await fetch(`${API_BASE}/achievements`);
  return res.json();
}

export async function getStreak(): Promise<StreakInfo> {
  if (USE_MOCK) return delay(mockStreak);
  const res = await fetch(`${API_BASE}/streak`);
  return res.json();
}
