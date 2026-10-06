import type { NextConfig } from "next";

// The browser only talks to Next.js; /api/* is forwarded to the FastAPI backend.
const API_URL = process.env.VANTAGE_API_URL ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${API_URL}/api/:path*` }];
  },
};

export default nextConfig;
