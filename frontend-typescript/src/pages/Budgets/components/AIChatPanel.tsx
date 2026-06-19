import React, { useState, useRef, useEffect } from "react";
import Button from "@/components/ui/Button";
import { streamParseBudget } from "@/api/budgetApi";
import { ParseBudgetResponse } from "../types/budget";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  isError?: boolean;
}

export const WELCOME_MESSAGE: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content:
    "Describe the budget you need and I'll generate a structured preview. You can keep refining it through conversation.",
};

interface Props {
  currentPreview: ParseBudgetResponse | null;
  onPreviewUpdate: (preview: ParseBudgetResponse) => void;
  onClose: () => void;
  messages: ChatMessage[];
  setMessages: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
}

export function AIChatPanel({ currentPreview, onPreviewUpdate, onClose, messages, setMessages }: Props) {
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamStatus, setStreamStatus] = useState("");
  const abortRef = useRef<AbortController | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamStatus]);

  const buildPrompt = (userMessage: string) => {
    if (!currentPreview) return userMessage;
    return `Current budget:\n${JSON.stringify(currentPreview)}\n\nUser request: ${userMessage}`;
  };

  const addMessage = (msg: Omit<ChatMessage, "id">) => {
    setMessages((prev) => [...prev, { ...msg, id: crypto.randomUUID() }]);
  };

  const handleSend = () => {
    const text = input.trim();
    if (!text || isStreaming) return;

    addMessage({ role: "user", content: text });
    setInput("");
    setIsStreaming(true);
    setStreamStatus("Starting...");

    abortRef.current = streamParseBudget(
      buildPrompt(text),
      (status) => setStreamStatus(status),
      (response) => {
        setIsStreaming(false);
        setStreamStatus("");
        onPreviewUpdate(response);
        addMessage({
          role: "assistant",
          content: currentPreview
            ? "Budget updated. Review the changes on the left and keep refining if needed."
            : "Here's your budget preview. Edit any field directly, then click Create Budget when ready.",
        });
      },
      (msg) => {
        setIsStreaming(false);
        setStreamStatus("");
        addMessage({
          role: "assistant",
          content: msg || "Something went wrong. Try rephrasing.",
          isError: true,
        });
      },
      () => {
        setIsStreaming(false);
        setStreamStatus("");
        addMessage({
          role: "assistant",
          content: "AI is not available right now.",
          isError: true,
        });
      }
    );
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-96 flex-shrink-0 border-l border-slate-200 bg-white flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold text-slate-800">
            AI Budget Assistant
          </span>
          <span className="w-2 h-2 rounded-full bg-green-400 flex-shrink-0" />
        </div>
        <Button
          variant="close"
          onClick={() => {
            abortRef.current?.abort();
            onClose();
          }}
        >
          ✕
        </Button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-3">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
                msg.role === "user"
                  ? "bg-slate-800 text-white rounded-br-sm"
                  : msg.isError
                    ? "bg-red-50 text-red-700 border border-red-200 rounded-bl-sm"
                    : "bg-slate-100 text-slate-800 rounded-bl-sm"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {isStreaming && (
          <div className="flex justify-start">
            <div className="bg-slate-100 rounded-2xl rounded-bl-sm px-4 py-2.5 text-sm text-slate-500 flex items-center gap-2">
              <div className="w-3 h-3 border-2 border-slate-300 border-t-slate-600 rounded-full animate-spin flex-shrink-0" />
              {streamStatus}
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-slate-200 p-4">
        <div className="flex items-end gap-2">
          <textarea
            rows={2}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isStreaming}
            placeholder={
              currentPreview
                ? "Refine the budget, e.g. 'add a travel line at $3k'..."
                : "Describe your budget..."
            }
            className="flex-1 resize-none border border-slate-300 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-400 disabled:opacity-50"
          />
          <Button
            variant="primary"
            onClick={handleSend}
            disabled={!input.trim() || isStreaming}
            className="px-3 py-2 shrink-0"
          >
            ↑
          </Button>
        </div>
        <p className="text-xs text-slate-400 mt-1.5">
          Enter to send · Shift+Enter for new line
        </p>
      </div>
    </div>
  );
}
