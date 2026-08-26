import { useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useAsyncData } from "../hooks/useAsyncData";
import { getAssessment, submitAssessmentAttempt } from "../services/api";
import { AssessmentAttempt } from "../types";
import LoadingState from "../components/common/LoadingState";
import ErrorState from "../components/common/ErrorState";
import ProgressBar from "../components/common/ProgressBar";
import Badge from "../components/common/Badge";
import QuestionCard from "../components/assessment/QuestionCard";

type Stage = "intro" | "in_progress" | "submitting" | "results";

export default function AssessmentPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const {
    data: assessment,
    loading,
    error,
    reload,
  } = useAsyncData(() => getAssessment(id ?? ""), [id]);

  const [stage, setStage] = useState<Stage>("intro");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [attempt, setAttempt] = useState<AssessmentAttempt | null>(null);

  if (loading) return <LoadingState label="Loading assessment" />;
  if (error) return <ErrorState message={error} onRetry={reload} />;
  if (!assessment) return null;

  const totalQuestions = assessment.questions.length;
  const currentQuestion = assessment.questions[currentIndex];
  const answeredCount = Object.keys(answers).length;
  const isLastQuestion = currentIndex === totalQuestions - 1;

  function handleSelect(optionId: string) {
    setAnswers((prev) => ({ ...prev, [currentQuestion.id]: optionId }));
  }

  function handleNext() {
    if (isLastQuestion) {
      handleSubmit();
    } else {
      setCurrentIndex((i) => i + 1);
    }
  }

  function handleBack() {
    setCurrentIndex((i) => Math.max(0, i - 1));
  }

  async function handleSubmit() {
    if (!id) return;
    setStage("submitting");
    const result = await submitAssessmentAttempt(id, answers);
    setAttempt(result);
    setStage("results");
  }

  function handleRetry() {
    setAnswers({});
    setCurrentIndex(0);
    setAttempt(null);
    setStage("intro");
  }

  // --- Intro screen ---------------------------------------------------
  if (stage === "intro") {
    return (
      <div className="container-form page-shell">
        <Link to={`/resource/${id}`} className="text-sm text-ink-700 hover:text-ink">
          ← Back
        </Link>

        <h1 className="mt-4 font-display text-3xl font-semibold text-ink">{assessment.title}</h1>

        <div className="mt-5 flex flex-wrap gap-2">
          {assessment.skillsTested.map((s) => (
            <Badge key={s}>{s}</Badge>
          ))}
        </div>

        <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3">
          <div className="rounded-xl2 border border-ink-700/10 bg-surface p-4">
            <p className="font-display text-2xl text-ink">{totalQuestions}</p>
            <p className="text-xs text-ink-700">Questions</p>
          </div>
          <div className="rounded-xl2 border border-ink-700/10 bg-surface p-4">
            <p className="font-display text-2xl text-ink">{assessment.passingScorePercent}%</p>
            <p className="text-xs text-ink-700">Passing score</p>
          </div>
          <div className="rounded-xl2 border border-ink-700/10 bg-surface p-4">
            <p className="font-display text-2xl text-ink">{Math.max(1, Math.round(totalQuestions * 1.5))}</p>
            <p className="text-xs text-ink-700">Minutes</p>
          </div>
        </div>

        <p className="mt-6 text-sm text-ink-700">
          You can move back and forth between questions before submitting. Your result is recorded
          once you submit, and you can retake this if you don't pass.
        </p>

        <button
          onClick={() => setStage("in_progress")}
          className="mt-8 btn-primary"
        >
          Start assessment
        </button>
      </div>
    );
  }

  // --- Submitting -------------------------------------------------------
  if (stage === "submitting") {
    return <LoadingState label="Scoring your answers" />;
  }

  // --- Results screen -----------------------------------------------------
  if (stage === "results" && attempt) {
    return (
      <div className="container-form page-shell">
        <div
          className={`rounded-xl2 border p-6 text-center ${
            attempt.passed ? "border-growth/30 bg-growth-light" : "border-clay/30 bg-clay-light"
          }`}
        >
          <p className={`font-mono text-xs uppercase tracking-wide ${attempt.passed ? "text-growth-dark" : "text-clay"}`}>
            {attempt.passed ? "Passed" : "Not yet"}
          </p>
          <p className="mt-2 font-display text-4xl font-semibold text-ink">
            {attempt.scorePercent}%
          </p>
          <p className="mt-1 text-sm text-ink-700">
            {attempt.correctCount} of {attempt.totalQuestions} correct — passing score is{" "}
            {assessment.passingScorePercent}%
          </p>
        </div>

        <div className="mt-6">
          <ProgressBar percent={attempt.scorePercent} label="Your score" />
        </div>

        <div className="mt-8 flex flex-wrap gap-3">
          {!attempt.passed && (
            <button
              onClick={handleRetry}
              className="btn-primary"
            >
              Retake assessment
            </button>
          )}
          <button
            onClick={() => navigate("/roadmap")}
            className="btn-secondary"
          >
            Back to roadmap
          </button>
        </div>
      </div>
    );
  }

  // --- In-progress question flow ----------------------------------------
  return (
    <div className="container-form page-shell">
      <ProgressBar percent={(answeredCount / totalQuestions) * 100} />

      <div className="mt-8">
        <QuestionCard
          question={currentQuestion}
          index={currentIndex}
          total={totalQuestions}
          selectedOptionId={answers[currentQuestion.id]}
          onSelect={handleSelect}
        />
      </div>

      <div className="mt-8 flex items-center justify-between">
        <button
          onClick={handleBack}
          disabled={currentIndex === 0}
          className="btn-secondary disabled:opacity-40"
        >
          Back
        </button>
        <button
          onClick={handleNext}
          disabled={!answers[currentQuestion.id]}
          className="btn-primary"
        >
          {isLastQuestion ? "Submit" : "Next"}
        </button>
      </div>
    </div>
  );
}
