// Client for the Vantage FastAPI backend, proxied under /api by next.config.ts.

export type AccessLevel = "public" | "interne" | "confidentiel";

export type RoleInfo = { id: string; levels: AccessLevel[] };

export type Source = {
  document_id: string;
  reference: string;
  portee: string;
  access_level: AccessLevel;
  heading: string;
  text: string;
  score: number;
};

export type ChatEvent =
  | { type: "sources"; sources: Source[] }
  | { type: "token"; text: string }
  | { type: "error"; message: string }
  | { type: "done"; refus: boolean };

export async function fetchRoles(): Promise<RoleInfo[]> {
  const response = await fetch("/api/roles");
  if (!response.ok) throw new Error(`GET /api/roles: ${response.status}`);
  return response.json();
}

/** Ask a question as a Rôle; events arrive as the server streams them. */
export async function streamChat(
  role: string,
  question: string,
  onEvent: (event: ChatEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role, question }),
    signal,
  });
  if (!response.ok || !response.body) throw new Error(`POST /api/chat: ${response.status}`);

  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = "";
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += value;
    let boundary: number;
    while ((boundary = buffer.indexOf("\n\n")) !== -1) {
      const block = buffer.slice(0, boundary);
      buffer = buffer.slice(boundary + 2);
      const event = parseEvent(block);
      if (event) onEvent(event);
    }
  }
}

function parseEvent(block: string): ChatEvent | null {
  let name = "";
  let data = "";
  for (const line of block.split("\n")) {
    if (line.startsWith("event: ")) name = line.slice(7);
    else if (line.startsWith("data: ")) data += line.slice(6);
  }
  const payload = data ? JSON.parse(data) : null;
  switch (name) {
    case "sources":
      return { type: "sources", sources: payload };
    case "token":
      return { type: "token", text: payload };
    case "error":
      return { type: "error", message: payload };
    case "done":
      return { type: "done", refus: Boolean(payload?.refus) };
    default:
      return null;
  }
}
