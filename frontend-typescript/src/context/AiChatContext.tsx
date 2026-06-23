import React, {
  createContext,
  useContext,
  useState,
  Dispatch,
  SetStateAction,
} from "react";
import {
  ChatMessage,
  WELCOME_MESSAGE,
} from "@/pages/Budgets/components/AIChatPanel";
import { Budget } from "@/pages/Budgets/types/budget";

interface AiChatContextType {
  isAiOpen: boolean;
  toggleAi: () => void;
  closeAi: () => void;
  messages: ChatMessage[];
  setMessages: Dispatch<SetStateAction<ChatMessage[]>>;
  contextBudget: Budget | null;
  setContextBudget: (b: Budget | null) => void;
}

const AiChatContext = createContext<AiChatContextType | undefined>(undefined);

export function AiChatProvider({ children }: { children: React.ReactNode }) {
  const [isAiOpen, setIsAiOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [contextBudget, setContextBudget] = useState<Budget | null>(null);

  const toggleAi = () => setIsAiOpen((v) => !v);
  const closeAi = () => setIsAiOpen(false);

  return (
    <AiChatContext.Provider
      value={{
        isAiOpen,
        toggleAi,
        closeAi,
        messages,
        setMessages,
        contextBudget,
        setContextBudget,
      }}
    >
      {children}
    </AiChatContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAiChat(): AiChatContextType {
  const ctx = useContext(AiChatContext);
  if (!ctx) throw new Error("useAiChat must be used within AiChatProvider");
  return ctx;
}
