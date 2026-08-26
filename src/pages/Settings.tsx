import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAsyncData } from "../hooks/useAsyncData";
import { getProfile, saveProfile, changePassword, deleteAccount } from "../services/api";
import { useAuth } from "../hooks/useAuth";
import { LearnerProfile, CareerGoal } from "../types";
import { careerOptions } from "../data/mockData";
import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import { useToast } from "../hooks/useToast";

type SavedBanner = "profile" | "password" | null;

export default function Settings() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { showToast } = useToast();
  const { data: profile, loading, error, reload } = useAsyncData(getProfile);

  const [form, setForm] = useState<LearnerProfile | null>(null);
  const [savingProfile, setSavingProfile] = useState(false);
  const [saved, setSaved] = useState<SavedBanner>(null);

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [savingPassword, setSavingPassword] = useState(false);

  const [confirmingDelete, setConfirmingDelete] = useState(false);
  const [deleteText, setDeleteText] = useState("");
  const [deleting, setDeleting] = useState(false);

  if (loading) return <LoadingState label="Loading your settings" />;
  if (error) return <ErrorState message={error} onRetry={reload} />;
  if (!profile) return null;

  const activeForm = form ?? profile;

  async function handleProfileSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSavingProfile(true);
    setSaved(null);
    await saveProfile(activeForm);
    setSavingProfile(false);
    setSaved("profile");
    showToast("Profile updated.", "growth");
    setTimeout(() => setSaved(null), 3000);
  }

  async function handlePasswordSubmit(e: React.FormEvent) {
    e.preventDefault();
    setPasswordError(null);

    if (newPassword.length < 6) {
      setPasswordError("New password must be at least 6 characters.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setPasswordError("New passwords don't match.");
      return;
    }

    setSavingPassword(true);
    try {
      await changePassword(currentPassword, newPassword);
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      setSaved("password");
      showToast("Password updated.", "growth");
      setTimeout(() => setSaved(null), 3000);
    } catch (err) {
      setPasswordError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setSavingPassword(false);
    }
  }

  async function handleDeleteAccount() {
    setDeleting(true);
    await deleteAccount();
    logout();
    navigate("/");
  }

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="container-narrow page-shell">
      <h1 className="text-page-title">Settings</h1>
      <p className="text-page-subtitle">Manage your profile, account, and preferences.</p>

      {/* --- Profile section --- */}
      <form
        onSubmit={handleProfileSubmit}
        className="mt-8 space-y-5 rounded-xl2 border border-ink-700/10 bg-surface p-6"
      >
        <p className="text-section-heading">Profile</p>

        <div>
          <label className="form-label">Name</label>
          <input
            value={activeForm.name}
            onChange={(e) => setForm({ ...activeForm, name: e.target.value })}
            className="input-field"
            required
          />
        </div>

        <div>
          <label className="form-label">Target career</label>
          <select
            value={activeForm.careerGoal}
            onChange={(e) => setForm({ ...activeForm, careerGoal: e.target.value as CareerGoal })}
            className="input-field"
          >
            {careerOptions.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
          <p className="mt-1 text-xs text-ink-700">
            Changing this will re-generate your roadmap and recommendations.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="form-label">Weekly hours</label>
            <input
              type="number"
              min={1}
              max={40}
              value={activeForm.weeklyHours}
              onChange={(e) => setForm({ ...activeForm, weeklyHours: Number(e.target.value) })}
              className="input-field"
            />
          </div>
          <div>
            <label className="form-label">Experience level</label>
            <select
              value={activeForm.experienceLevel}
              onChange={(e) =>
                setForm({ ...activeForm, experienceLevel: e.target.value as LearnerProfile["experienceLevel"] })
              }
              className="input-field"
            >
              <option>Beginner</option>
              <option>Intermediate</option>
              <option>Advanced</option>
            </select>
          </div>
        </div>

        <div>
          <label className="form-label">
            Preferences <span className="text-ink-700/60">(optional)</span>
          </label>
          <input
            value={activeForm.preferences ?? ""}
            onChange={(e) => setForm({ ...activeForm, preferences: e.target.value })}
            placeholder="e.g. prefer hands-on projects over lectures"
            className="input-field"
          />
        </div>

        <div className="flex items-center gap-3">
          <button
            type="submit"
            disabled={savingProfile}
            className="btn-primary"
          >
            {savingProfile ? "Saving…" : "Save changes"}
          </button>
          {saved === "profile" && <span className="text-sm text-growth-dark">Saved.</span>}
        </div>
      </form>

      {/* --- Account section --- */}
      <div className="mt-6 space-y-5 rounded-xl2 border border-ink-700/10 bg-surface p-6">
        <p className="text-section-heading">Account</p>

        <div>
          <label className="form-label">Email</label>
          <input
            value={user?.email ?? ""}
            disabled
            className="input-field-disabled"
          />
        </div>

        <form onSubmit={handlePasswordSubmit} className="space-y-4 border-t border-ink-700/10 pt-4">
          <p className="text-sm font-medium text-ink">Change password</p>

          {passwordError && (
            <p className="rounded-xl2 border border-clay/30 bg-clay-light px-3 py-2 text-sm text-clay">
              {passwordError}
            </p>
          )}

          <input
            type="password"
            required
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            placeholder="Current password"
            className="input-field"
          />
          <input
            type="password"
            required
            minLength={6}
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            placeholder="New password"
            className="input-field"
          />
          <input
            type="password"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm new password"
            className="input-field"
          />

          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={savingPassword}
              className="btn-secondary"
            >
              {savingPassword ? "Updating…" : "Update password"}
            </button>
            {saved === "password" && <span className="text-sm text-growth-dark">Password updated.</span>}
          </div>
        </form>

        <div className="border-t border-ink-700/10 pt-4">
          <button
            onClick={handleLogout}
            className="btn-secondary"
          >
            Log out
          </button>
        </div>
      </div>

      {/* --- Danger zone --- */}
      <div className="mt-6 rounded-xl2 border border-clay/30 bg-clay-light p-6">
        <p className="text-section-heading text-clay">Danger zone</p>
        <p className="mt-1 text-sm text-ink-700">
          Deleting your account permanently removes your profile, roadmap, and progress. This can't
          be undone.
        </p>

        {!confirmingDelete ? (
          <button
            onClick={() => setConfirmingDelete(true)}
            className="mt-4 rounded-full border border-clay px-5 py-2 text-sm font-medium text-clay transition hover:bg-clay hover:text-white"
          >
            Delete account
          </button>
        ) : (
          <div className="mt-4 space-y-3">
            <p className="text-sm text-ink">
              Type <span className="font-mono font-semibold">DELETE</span> to confirm.
            </p>
            <input
              value={deleteText}
              onChange={(e) => setDeleteText(e.target.value)}
              className="w-full max-w-xs rounded-xl2 border border-clay/40 bg-surface px-3 py-2 text-sm outline-none focus:border-clay"
            />
            <div className="flex gap-3">
              <button
                onClick={handleDeleteAccount}
                disabled={deleteText !== "DELETE" || deleting}
                className="rounded-full bg-clay px-5 py-2 text-sm font-medium text-white transition hover:opacity-90 disabled:opacity-40"
              >
                {deleting ? "Deleting…" : "Permanently delete"}
              </button>
              <button
                onClick={() => {
                  setConfirmingDelete(false);
                  setDeleteText("");
                }}
                className="rounded-full border border-ink-700/20 px-5 py-2 text-sm text-ink-700 transition hover:bg-ink-700/10"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
