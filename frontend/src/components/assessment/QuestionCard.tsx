import { AssessmentQuestion } from "../../types";

interface QuestionCardProps {
  question: AssessmentQuestion;
  index: number;
  total: number;
  selectedOptionId?: string;
  onSelect: (optionId: string) => void;
}

export default function QuestionCard({
  question,
  index,
  total,
  selectedOptionId,
  onSelect,
}: QuestionCardProps) {
  return (
    <div>
      <p className="font-mono text-xs uppercase tracking-wide text-ink-700/70">
        Question {index + 1} of {total}
      </p>
      <p className="mt-2 font-display text-xl text-ink">{question.prompt}</p>

      <div className="mt-5 space-y-2.5">
        {question.options.map((opt) => {
          const isSelected = selectedOptionId === opt.id;
          return (
            <button
              key={opt.id}
              onClick={() => onSelect(opt.id)}
              className={`flex w-full items-center gap-3 rounded-xl2 border px-4 py-3 text-left text-sm transition ${
                isSelected
                  ? "border-growth bg-growth-light text-ink"
                  : "border-ink-700/15 bg-surface text-ink-700 hover:border-ink-700/30"
              }`}
            >
              <span
                className={`flex h-5 w-5 flex-none items-center justify-center rounded-full border text-[11px] ${
                  isSelected
                    ? "border-growth bg-growth text-white"
                    : "border-ink-700/30 text-transparent"
                }`}
              >
                ✓
              </span>
              {opt.text}
            </button>
          );
        })}
      </div>
    </div>
  );
}
