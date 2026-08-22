"use client";

import { Lightbulb } from "lucide-react";
import Link from "next/link";
import skillsData from "@/services/skills.json";
import { useI18n } from "@/i18n/provider";

export default function SkillsPage() {
    const { t } = useI18n();
    // Group skills by category
    const skillsByCategory = skillsData.reduce((acc, skill) => {
        if (!acc[skill.category]) {
            acc[skill.category] = [];
        }
        acc[skill.category].push(skill);
        return acc;
    }, {} as Record<string, typeof skillsData>);

    // Order of categories to display
    const categoryOrder = [
        "Frontend & UI",
        "Backend & API",
        "Database",
        "Cloud & Infrastructure",
        "Testing & Quality",
        "Security",
        "Architecture & Planning",
        "Mobile",
        "Game Development",
        "SEO & Growth",
        "Research",
        "Shell/CLI",
        "Orchestration & Memory",
        "Other"
    ];

    return (
        <div className="max-w-3xl">
            {/* Breadcrumb */}
            <nav className="flex items-center gap-2 text-sm text-muted-foreground mb-6">
                <Link href="/docs" className="hover:text-foreground">{t.skillsPage.breadcrumbDocs}</Link>
                <span>/</span>
                <span className="text-foreground">{t.skillsPage.breadcrumbCurrent}</span>
            </nav>

            {/* Page Header */}
            <div className="mb-8 pb-8 border-b border-border">
                <h1 className="text-4xl font-bold tracking-tight text-foreground mb-4">
                    {t.skillsPage.title}
                </h1>
                <p className="text-lg text-muted-foreground">
                    {t.skillsPage.subtitle}
                </p>
            </div>

            {/* What are Skills */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.skillsPage.whatTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-4">
                    {t.skillsPage.whatP1}
                </p>
                <p className="text-base text-muted-foreground mb-6">
                    {t.skillsPage.whatP2a}<em>{t.skillsPage.whatP2Em}</em>{t.skillsPage.whatP2b}
                </p>
                <div className="mt-2 p-4 rounded-lg border border-blue-200 dark:border-blue-900 bg-blue-50 dark:bg-blue-950/20 mb-6">
                    <p className="text-sm text-blue-900 dark:text-blue-100 mb-0">
                        <Lightbulb className="w-4 h-4 inline" />
                        <strong className="font-semibold">{t.skillsPage.noteStrong}</strong>{t.skillsPage.noteText}
                    </p>
                </div>
            </section>

            {/* How Skills Work */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.skillsPage.howTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-6">
                    {t.skillsPage.howP}
                </p>

                <ul className="space-y-3 mb-6">
                    <li className="flex items-start gap-3 text-base text-muted-foreground">
                        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-primary text-primary-foreground text-xs font-bold shrink-0 mt-0.5">1</span>
                        <div>
                            <strong className="font-semibold text-foreground">{t.skillsPage.step1Title}</strong>
                            <p className="text-sm mt-1">{t.skillsPage.step1Desc}</p>
                        </div>
                    </li>
                    <li className="flex items-start gap-3 text-base text-muted-foreground">
                        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-primary text-primary-foreground text-xs font-bold shrink-0 mt-0.5">2</span>
                        <div>
                            <strong className="font-semibold text-foreground">{t.skillsPage.step2Title}</strong>
                            <p className="text-sm mt-1">{t.skillsPage.step2Desc}</p>
                        </div>
                    </li>
                    <li className="flex items-start gap-3 text-base text-muted-foreground">
                        <span className="flex items-center justify-center w-6 h-6 rounded-full bg-primary text-primary-foreground text-xs font-bold shrink-0 mt-0.5">3</span>
                        <div>
                            <strong className="font-semibold text-foreground">{t.skillsPage.step3Title}</strong>
                            <p className="text-sm mt-1">{t.skillsPage.step3Desc}</p>
                        </div>
                    </li>
                </ul>
            </section>

            {/* Skill Categories */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.skillsPage.categoriesTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-6">
                    {skillsData.length}{t.skillsPage.categoriesPb}
                </p>

                <div className="space-y-8">
                    {categoryOrder.map((category) => {
                        const skills = skillsByCategory[category];
                        if (!skills) return null;

                        return (
                            <div key={category}>
                                <h3 className="text-lg font-semibold text-foreground mb-4 border-b border-border pb-2 inline-block">
                                    {category}
                                </h3>
                                <div className="grid gap-3 sm:grid-cols-2">
                                    {skills.map((skill) => (
                                        <div key={skill.name} className="p-4 rounded-lg border border-border bg-card hover:border-border transition-colors">
                                            <code className="text-sm font-mono text-foreground font-semibold block mb-1">
                                                {skill.name}
                                            </code>
                                            <p className="text-xs text-muted-foreground">
                                                {skill.description}
                                            </p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </section>

            {/* Skill Structure */}
            <section className="mb-12">
                <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
                    {t.skillsPage.structureTitle}
                </h2>
                <p className="text-base text-muted-foreground mb-6">
                    {t.skillsPage.structureP}
                </p>

                <div className="relative group mb-6">
                    <pre className="p-4 rounded-lg bg-code overflow-x-auto border border-code-border font-mono text-sm">
                        <code className="text-code-foreground">{`skills/
└── nextjs-react-expert/
    ├── SKILL.md         # Main documentation
    ├── sections/        # Detailed guides
    ├── examples/        # Reference implementations
    └── scripts/         # Helper utilities (optional)`}</code>
                    </pre>
                </div>
            </section>

            


            
        </div>
    );
}
