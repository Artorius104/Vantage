"use client";

import dynamic from "next/dynamic";

// The chat reads its Conversations from browser storage, so it is never server-rendered.
export const ClientChat = dynamic(() => import("./ChatApp").then((m) => m.ChatApp), { ssr: false });
