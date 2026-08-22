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

export const metadata: Metadata = {
  title: "AG Kit - AI Agent Capability Expansion Toolkit",
  description:
    "A comprehensive collection of 48 skills, 20 specialist agents, rules, and production-ready workflows for modern AI coding assistants.",
  metadataBase: new URL("https://ag-kit.unikorn.vn/"),
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
    images: [
      {
        url: "/images/og-image.png",
        width: 1280,
        height: 640,
        alt: "AG Kit — Antigravity agent engineering kit",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "AG Kit - AI Agent Capability Expansion Toolkit",
    description:
      "Skills, specialist agents, rules, and production-ready workflows for modern AI coding assistants.",
    images: ["/images/og-image.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className="antialiased"
      >
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
