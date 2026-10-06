"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { Source } from "@/lib/api";
import type { Message } from "@/lib/conversations";
import { SourceList, sourceAnchor } from "./SourceList";

export function MessageView({ message }: { message: Message }) {
  if (message.author === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] whitespace-pre-wrap rounded-2xl bg-neutral-800 px-4 py-2.5 text-[15px] text-neutral-100">
          {message.content}
        </div>
      </div>
    );
  }

  const sources = message.sources ?? [];
  return (
    <div className="flex gap-3">
      <div className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-sky-600 text-xs font-semibold text-white">
        V
      </div>
      <div className="min-w-0 flex-1">
        <div className="prose-vantage text-[15px] leading-relaxed text-neutral-200">
          {message.content ? (
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                a: ({ href, children }) =>
                  href?.startsWith("#src-") ? (
                    <a
                      href={href}
                      className="mx-0.5 rounded-md bg-sky-500/15 px-1.5 py-0.5 text-xs font-medium text-sky-300 no-underline ring-1 ring-inset ring-sky-500/30 hover:bg-sky-500/25"
                    >
                      {children}
                    </a>
                  ) : (
                    <a href={href} className="text-sky-400 underline" target="_blank" rel="noreferrer">
                      {children}
                    </a>
                  ),
              }}
            >
              {linkCitations(message.content, sources, message.id)}
            </ReactMarkdown>
          ) : (
            <span className="inline-flex gap-1 py-2" aria-label="Réponse en cours">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-neutral-500" />
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-neutral-500 [animation-delay:150ms]" />
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-neutral-500 [animation-delay:300ms]" />
            </span>
          )}
          {message.status === "streaming" && message.content && (
            <span className="ml-0.5 inline-block h-4 w-1.5 animate-pulse bg-neutral-400 align-middle" />
          )}
        </div>
        {message.status === "error" && (
          <p className="mt-2 text-sm text-rose-400">La réponse a échoué. Vérifiez que l’API et le modèle tournent.</p>
        )}
        {message.status !== "streaming" && <SourceList sources={sources} messageId={message.id} />}
      </div>
    </div>
  );
}

/** Turn "[Référence]" into a link to its source card, when the Référence was actually retrieved. */
function linkCitations(content: string, sources: Source[], messageId: string): string {
  return content.replace(/\[([^\[\]\n]+)\](?!\()/g, (match, reference: string) => {
    const index = sources.findIndex((source) => source.reference === reference.trim());
    return index === -1 ? match : `[${reference}](#${sourceAnchor(messageId, index)})`;
  });
}
