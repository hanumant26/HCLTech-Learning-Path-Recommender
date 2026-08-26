import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./hooks/useAuth";
import { ThemeProvider } from "./hooks/useTheme";
import { ToastProvider } from "./hooks/useToast";
import RequireAuth from "./components/layout/RequireAuth";
import Layout from "./components/layout/Layout";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import CareerExploration from "./pages/CareerExploration";
import Onboarding from "./pages/Onboarding";
import Welcome from "./pages/Welcome";
import SkillAssessment from "./pages/SkillAssessment";
import Recommendations from "./pages/Recommendations";
import CourseCatalog from "./pages/CourseCatalog";
import LearningRoadmap from "./pages/LearningRoadmap";
import ResourceDetails from "./pages/ResourceDetails";
import AssessmentPage from "./pages/AssessmentPage";
import ProgressDashboard from "./pages/ProgressDashboard";
import ActivityLog from "./pages/ActivityLog";
import Achievements from "./pages/Achievements";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <ThemeProvider>
      <ToastProvider>
        <AuthProvider>
          <Routes>
            {/* Public routes — no navbar/assistant chrome */}
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/careers" element={<CareerExploration />} />

            {/* Everything else requires a session */}
            <Route element={<RequireAuth />}>
              <Route element={<Layout />}>
                <Route path="/profile" element={<Onboarding />} />
                <Route path="/welcome" element={<Welcome />} />
                <Route path="/skill-assessment" element={<SkillAssessment />} />
                <Route path="/recommendations" element={<Recommendations />} />
                <Route path="/courses" element={<CourseCatalog />} />
                <Route path="/roadmap" element={<LearningRoadmap />} />
                <Route path="/resource/:id" element={<ResourceDetails />} />
                <Route path="/assessment/:id" element={<AssessmentPage />} />
                <Route path="/progress" element={<ProgressDashboard />} />
                <Route path="/activity" element={<ActivityLog />} />
                <Route path="/achievements" element={<Achievements />} />
                <Route path="/settings" element={<Settings />} />
              </Route>
            </Route>
          </Routes>
        </AuthProvider>
      </ToastProvider>
    </ThemeProvider>
  );
}
