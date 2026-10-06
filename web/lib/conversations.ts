// Conversations live in the browser for now, one list per Rôle (ADR 0002):
// switching Rôle switches lists and never carries a Conversation across.
// Server-side storage comes with issue #16.

import type { Source } from "./api";

export type Message = {
  id: string;
  author: "user" | "assistant";
  content: string;
  sources?: Source[];
  status?: "streaming" | "done" | "error";
};

export type Conversation = {
  id: string;
  title: string;
  updatedAt: number;
  messages: Message[];
};

export type ConversationsByRole = Record<string, Conversation[]>;

const STORAGE_KEY = "vantage.conversations.v1";

export function loadConversations(): ConversationsByRole {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    const stored: ConversationsByRole = raw ? JSON.parse(raw) : {};
    // An answer still streaming when the page was closed will never finish.
    for (const list of Object.values(stored))
      for (const conversation of list)
        for (const message of conversation.messages) if (message.status === "streaming") message.status = "error";
    return stored;
  } catch {
    return {};
  }
}

export function saveConversations(conversations: ConversationsByRole): void {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
  } catch {
    // Storage full or blocked: the session keeps working in memory.
  }
}

export function newId(): string {
  return crypto.randomUUID();
}

export function createConversation(firstQuestion: string): Conversation {
  return { id: newId(), title: titleFrom(firstQuestion), updatedAt: Date.now(), messages: [] };
}

function titleFrom(question: string): string {
  const title = question.trim().replace(/\s+/g, " ");
  return title.length > 48 ? `${title.slice(0, 47)}…` : title;
}
