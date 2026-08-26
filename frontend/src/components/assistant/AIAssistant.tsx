import { useState, useRef, useEffect } from "react";
import { ChatMessage } from "../../types";
import { askAssistant } from "../../services/api";

const suggestedPrompts = [
  "Why was this recommended?",
  "What should I learn next?",
  "I only have 5 hours this week.",
];

export default function AIAssistant() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      content: "Hi! I'm your learning assistant. Ask me about your roadmap, recommendations, or what to focus on next.",
    },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, open]);

  async function handleSend(text: string) {
    if (!text.trim() || sending) return;
    const userMsg: ChatMessage = { id: crypto.randomUUID(), role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setSending(true);
    try {
      const reply = await askAssistant(text);
      setMessages((prev) => [...prev, reply]);
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="fixed bottom-5 right-5 z-50">
      {open && (
        <div className="mb-3 flex h-[28rem] w-80 flex-col overflow-hidden rounded-xl2 border border-ink-700/10 bg-surface shadow-xl sm:w-96">
          <div className="flex items-center justify-between bg-ink px-4 py-3">
            <span className="font-display text-sm font-medium text-paper">AI Learning Assistant</span>
            <button
              onClick={() => setOpen(false)}
              className="text-paper/70 transition hover:text-paper"
              aria-label="Close assistant"
            >
              ✕
            </button>
          </div>

          <div ref={scrollRef} className="flex-1 space-y-3 overflow-y-auto px-4 py-3">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`max-w-[85%] rounded-xl2 px-3 py-2 text-sm ${
                  m.role === "user"
                    ? "ml-auto bg-growth text-white"
                    : "bg-ink-700/10 text-ink"
                }`}
              >
                {m.content}
              </div>
            ))}
            {sending && <div className="text-xs text-ink-700">Assistant is typing…</div>}
          </div>

          <div className="border-t border-ink-700/10 px-3 py-2">
            <div className="mb-2 flex flex-wrap gap-1.5">
              {suggestedPrompts.map((p) => (
                <button
                  key={p}
                  onClick={() => handleSend(p)}
                  className="rounded-full border border-ink-700/20 px-2.5 py-1 text-[11px] text-ink-700 transition hover:bg-ink-700/10"
                >
                  {p}
                </button>
              ))}
            </div>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend(input);
              }}
              className="flex gap-2"
            >
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a question…"
                className="flex-1 rounded-full border border-ink-700/20 bg-paper px-3 py-2 text-sm outline-none focus:border-growth"
              />
              <button
                type="submit"
                disabled={sending}
                className="rounded-full bg-ink px-3 py-2 text-sm text-paper transition hover:bg-ink-700 disabled:opacity-50"
              >
                Send
              </button>
            </form>
          </div>
        </div>
      )}

      <button
        onClick={() => setOpen((o) => !o)}
        className="flex h-14 w-14 items-center justify-center rounded-full bg-ink text-paper shadow-lg transition hover:bg-ink-700"
        aria-label="Toggle AI assistant"
      >
        {open ? "✕" : "💬"}
      </button>
    </div>
  );
}
