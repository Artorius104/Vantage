"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { fetchRoles, streamChat, type RoleInfo } from "@/lib/api";
import {
  createConversation,
  loadConversations,
  newId,
  saveConversations,
  type Conversation,
  type ConversationsByRole,
  type Message,
} from "@/lib/conversations";
import { Composer } from "./Composer";
import { MessageView } from "./MessageView";
import { Sidebar } from "./Sidebar";

const SUGGESTIONS = [
  "Une IA utilisée pour trier des candidatures est-elle à haut risque ?",
  "Quel rôle approuve un risque résiduel A3 ?",
  "Quel est le délai interne visé pour une notification de sécurité aérienne ?",
  "Quel projet a rencontré un problème sur surface humide ?",
];

export function ChatApp() {
  const [roles, setRoles] = useState<RoleInfo[]>([]);
  const [apiError, setApiError] = useState<string | null>(null);
  const [role, setRole] = useState("Employé");
  // Rendered client-side only (see ClientChat), so browser storage is readable here.
  const [conversations, setConversations] = useState<ConversationsByRole>(loadConversations);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const abort = useRef<AbortController | null>(null);
  const bottom = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchRoles()
      .then(setRoles)
      .catch(() => setApiError("L’API Vantage ne répond pas. Lancez `uvicorn vantage.api.app:app` sur le port 8000."));
  }, []);

  useEffect(() => saveConversations(conversations), [conversations]);

  const list = conversations[role] ?? [];
  const active = list.find((c) => c.id === activeId) ?? null;

  useEffect(() => {
    bottom.current?.scrollIntoView({ block: "end" });
  }, [active?.messages]);

  const updateConversation = useCallback(
    (forRole: string, id: string, update: (c: Conversation) => Conversation) => {
      setConversations((all) => ({
        ...all,
        [forRole]: (all[forRole] ?? []).map((c) => (c.id === id ? update(c) : c)),
      }));
    },
    [],
  );

  const updateMessage = (forRole: string, conversationId: string, messageId: string, update: (m: Message) => Message) =>
    updateConversation(forRole, conversationId, (c) => ({
      ...c,
      updatedAt: Date.now(),
      messages: c.messages.map((m) => (m.id === messageId ? update(m) : m)),
    }));

  const send = async (question: string) => {
    const askedRole = role;
    let conversationId = activeId;
    if (!active) {
      const conversation = createConversation(question);
      conversationId = conversation.id;
      setConversations((all) => ({ ...all, [askedRole]: [...(all[askedRole] ?? []), conversation] }));
      setActiveId(conversationId);
    }
    const userMessage: Message = { id: newId(), author: "user", content: question };
    const reply: Message = { id: newId(), author: "assistant", content: "", status: "streaming" };
    updateConversation(askedRole, conversationId!, (c) => ({
      ...c,
      updatedAt: Date.now(),
      messages: [...c.messages, userMessage, reply],
    }));

    setBusy(true);
    abort.current = new AbortController();
    try {
      await streamChat(
        askedRole,
        question,
        (event) => {
          if (event.type === "sources") updateMessage(askedRole, conversationId!, reply.id, (m) => ({ ...m, sources: event.sources }));
          else if (event.type === "token")
            updateMessage(askedRole, conversationId!, reply.id, (m) => ({ ...m, content: m.content + event.text }));
          else if (event.type === "error") updateMessage(askedRole, conversationId!, reply.id, (m) => ({ ...m, status: "error" }));
          // A Refus cites nothing: listing what was searched would only confuse.
          else if (event.type === "done" && event.refus)
            updateMessage(askedRole, conversationId!, reply.id, (m) => ({ ...m, sources: [] }));
        },
        abort.current.signal,
      );
      updateMessage(askedRole, conversationId!, reply.id, (m) => (m.status === "error" ? m : { ...m, status: "done" }));
    } catch (error) {
      const stopped = error instanceof DOMException && error.name === "AbortError";
      updateMessage(askedRole, conversationId!, reply.id, (m) => ({ ...m, status: stopped ? "done" : "error" }));
    } finally {
      setBusy(false);
      abort.current = null;
    }
  };

  const changeRole = (next: string) => {
    abort.current?.abort();
    setRole(next);
    setActiveId(null);
  };

  const deleteConversation = (id: string) => {
    setConversations((all) => ({ ...all, [role]: (all[role] ?? []).filter((c) => c.id !== id) }));
    if (id === activeId) setActiveId(null);
  };

  return (
    <div className="flex h-dvh bg-neutral-900 text-neutral-100">
      <Sidebar
        roles={roles}
        role={role}
        conversations={list}
        activeId={activeId}
        onRoleChange={changeRole}
        onSelect={setActiveId}
        onNew={() => setActiveId(null)}
        onDelete={deleteConversation}
      />

      <main className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-12 items-center gap-2 border-b border-neutral-800/80 px-5 text-sm text-neutral-400">
          <span className="truncate text-neutral-200">{active?.title ?? "Nouvelle conversation"}</span>
          <span className="ml-auto rounded-full bg-neutral-800 px-2.5 py-0.5 text-xs text-neutral-300">{role}</span>
        </header>

        {apiError && <div className="bg-rose-950/60 px-5 py-2 text-sm text-rose-300">{apiError}</div>}

        <div className="flex-1 overflow-y-auto">
          {active && active.messages.length > 0 ? (
            <div className="mx-auto max-w-3xl space-y-6 px-5 py-8">
              {active.messages.map((message) => (
                <MessageView key={message.id} message={message} />
              ))}
              <div ref={bottom} />
            </div>
          ) : (
            <div className="mx-auto flex h-full max-w-3xl flex-col justify-center px-5 pb-16">
              <h1 className="text-3xl font-semibold text-neutral-100">Bonjour</h1>
              <p className="mt-2 text-neutral-400">
                Vous êtes connecté en tant que <span className="text-neutral-200">{role}</span>. Vantage répond uniquement à
                partir des documents que ce rôle peut consulter.
              </p>
              <div className="mt-8 grid gap-2 sm:grid-cols-2">
                {SUGGESTIONS.map((suggestion) => (
                  <button
                    key={suggestion}
                    type="button"
                    disabled={busy || roles.length === 0}
                    onClick={() => send(suggestion)}
                    className="rounded-xl border border-neutral-800 bg-neutral-900 px-4 py-3 text-left text-sm text-neutral-300 hover:border-neutral-700 hover:bg-neutral-800/60 disabled:opacity-50"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="mx-auto w-full max-w-3xl px-5 pb-5">
          <Composer disabled={roles.length === 0} busy={busy} onSend={send} onStop={() => abort.current?.abort()} />
          <p className="mt-2 text-center text-[11px] text-neutral-600">
            Vantage cite ses sources. Vérifiez les Références avant toute décision.
          </p>
        </div>
      </main>
    </div>
  );
}
