import type { Metadata, Viewport } from "next";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { I18nProvider } from "@/i18n/provider";

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "white" },
    { media: "(prefers-color-scheme: dark)", color: "black" },
  ],
  width: "device-width",
  initialScale: 1,
};

const description =
  "A lean multi-runtime operating layer for AI coding agents with a tiny shared core, 18 hot-loaded skills, four permanent agents, local-first memory, MCP, preflight gates, and read-only cross-audit.";

export const metadata: Metadata = {
  title: {
    default: "AG Kit - Lean Multi-Runtime Agent Operating Layer",
    template: "%s | AG Kit",
  },
  description,
  metadataBase: new URL("https://ag-kit.unikorn.vn/"),
  manifest: "/manifest.webmanifest",
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/images/logo.svg", type: "image/svg+xml" },
    ],
    apple: [{ url: "/images/logo.png", sizes: "1024x1024", type: "image/png" }],
  },
  robots: {
    index: true,
    follow: true,
  },
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://ag-kit.unikorn.vn/",
    siteName: "AG Kit",
    title: "AG Kit - Lean Multi-Runtime Agent Operating Layer",
    description,
    images: [
      {
        url: "/images/og-image.png",
        width: 1280,
        height: 640,
        alt: "AG Kit — lean multi-runtime agent operating layer",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "AG Kit - Lean Multi-Runtime Agent Operating Layer",
    description,
    images: ["/images/og-image.png"],
  },
};

const jsonLd = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://ag-kit.unikorn.vn/#website",
      url: "https://ag-kit.unikorn.vn/",
      name: "AG Kit",
      description,
      inLanguage: "en-US",
    },
    {
      "@type": "SoftwareApplication",
      "@id": "https://ag-kit.unikorn.vn/#software",
      name: "AG Kit",
      applicationCategory: "DeveloperApplication",
      operatingSystem: "Cross-platform",
      offers: {
        "@type": "Offer",
        price: "0",
        priceCurrency: "USD",
      },
      description,
      url: "https://ag-kit.unikorn.vn/",
      downloadUrl: "https://www.npmjs.com/package/@vudovn/ag-kit",
      softwareVersion: "2026.8.31",
      author: {
        "@type": "Organization",
        name: "AG Kit Team",
        url: "https://github.com/vudovn/ag-kit",
      },
    },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        <a
          href="#main-content"
          className="sr-only fixed left-4 top-4 z-[100] rounded-md bg-primary px-4 py-2 text-primary-foreground shadow focus:not-sr-only"
        >
          Skip to main content
        </a>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          <I18nProvider>{children}</I18nProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
