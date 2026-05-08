import type { NextConfig } from "next";
import createMDX from "@next/mdx";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = dirname(fileURLToPath(import.meta.url));

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        hostname: "img.vietqr.io",
        protocol: "https",
      },
    ],
  },
  output: "standalone",
  pageExtensions: ["js", "jsx", "md", "mdx", "ts", "tsx"],
  reactCompiler: true,
  turbopack: {
    root: appRoot,
  },
};

const withMDX = createMDX({});

export default withMDX(nextConfig);
