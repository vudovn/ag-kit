import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "AG Kit - Lean Multi-Runtime Agent Operating Layer",
    short_name: "AG Kit",
    description:
      "Tiny shared core, hot-loaded skills, local-first memory, MCP, specialist teams, preflight gates, and read-only cross-audit for modern AI coding agents.",
    start_url: "/",
    display: "standalone",
    background_color: "#09090b",
    theme_color: "#2dd4bf",
    icons: [
      {
        src: "/favicon.ico",
        sizes: "any",
        type: "image/x-icon",
      },
      {
        src: "/images/logo.svg",
        sizes: "any",
        type: "image/svg+xml",
      },
      {
        src: "/images/logo.png",
        sizes: "1024x1024",
        type: "image/png",
      },
    ],
  };
}
