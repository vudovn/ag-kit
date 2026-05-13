import type { Metadata } from "next";
import DocsSidebar from "@/components/docs/sidebar";
import Header from "@/components/layout/header";
import Footer from "@/components/layout/footer";

export const metadata: Metadata = {
    title: "Documentation | AG Kit",
    description: "Complete documentation for AG Kit - AI Agent templates with Skills, Agents, and Workflows.",
};

export default function DocsLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen bg-white dark:bg-zinc-950 flex flex-col">
            {/* Header */}
            <Header />

            <div className="container mx-auto px-4 sm:px-6 lg:px-8 flex-1">
                <div className="flex gap-8 lg:gap-12">
                    {/* Sidebar Navigation - Desktop */}
                    <aside className="hidden lg:block w-64 shrink-0 sticky top-[57px] h-[calc(100vh-3.5rem)] overflow-y-auto py-8 scrollbar-thin">
                        <DocsSidebar />
                    </aside>

                    {/* Main Content Area */}
                    <main className="flex-1 min-w-0 py-8 lg:py-10 max-w-4xl">
                        {children}
                    </main>

                    {/* Right Sidebar - Table of Contents */}
                    <aside className="hidden xl:block w-64 shrink-0 sticky top-[57px] h-[calc(100vh-3.5rem)] overflow-y-auto py-8 scrollbar-thin">
                        <div className="text-sm">
                            <div className="font-semibold text-zinc-900 dark:text-zinc-50 mb-3">
                                On This Page
                            </div>
                            <div className="text-xs text-zinc-500 dark:text-zinc-500">
                                Table of contents coming soon
                            </div>
                        </div>
                    </aside>
                </div>
            </div>

            {/* Footer */}
            <Footer />
        </div>
    );
}
