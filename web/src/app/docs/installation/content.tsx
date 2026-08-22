"use client";

import Link from "next/link";
import { Callout } from "@/components/mdx";
import { useI18n } from "@/i18n/provider";

export default function InstallationContent() {
  const { t } = useI18n();
  return (
    <div className="max-w-3xl">
      <nav className="flex items-center gap-2 text-sm text-muted-foreground mb-6">
        <Link href="/docs" className="hover:text-foreground">{t.installPage.breadcrumbDocs}</Link>
        <span>/</span>
        <span className="text-foreground">{t.installPage.breadcrumbCurrent}</span>
      </nav>

      <div className="mb-8 pb-8 border-b border-border">
        <h1 className="text-4xl font-bold tracking-tight text-foreground mb-4">
          {t.installPage.title}
        </h1>
        <p className="text-lg text-muted-foreground">
          {t.installPage.subtitle}
        </p>
      </div>

      <section id="quick-start" className="mb-12 scroll-mt-16">
        <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
          {t.installPage.quickStartTitle}
        </h2>
        <p className="text-base text-muted-foreground mb-6">
          {t.installPage.quickStartPa}<code className="px-1.5 py-0.5 rounded bg-muted text-sm font-mono">npx</code>{t.installPage.quickStartPb}
        </p>

        <pre className="p-4 rounded-lg bg-code overflow-x-auto mb-4 text-sm font-mono text-code-foreground">
          npx @vudovn/ag-kit init
        </pre>

        <Callout type="info">
          <strong>{t.installPage.calloutNoteStrong}</strong>{t.installPage.calloutNoteA}<code>.agents</code>{t.installPage.calloutNoteB}
        </Callout>
      </section>

      <section id="global-install" className="mb-12 scroll-mt-16">
        <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
          {t.installPage.globalTitle}
        </h2>
        <p className="text-base text-muted-foreground mb-6">
          {t.installPage.globalPa}<code className="px-1.5 py-0.5 rounded bg-muted text-sm font-mono">ag-kit</code>{t.installPage.globalPb}
        </p>

        <pre className="p-4 rounded-lg bg-code overflow-x-auto mb-2 text-sm font-mono text-code-foreground">
          npm install -g @vudovn/ag-kit
        </pre>

        <pre className="p-4 rounded-lg bg-code overflow-x-auto mb-4 text-sm font-mono text-code-foreground">
          cd your-project && ag-kit init
        </pre>

        <p className="text-sm text-muted-foreground mb-4">
          {t.installPage.globalReadOtherA}<Link className="text-blue-500 hover:text-blue-600 dark:text-blue-400 dark:hover:text-blue-300" href="/docs/cli">{t.installPage.globalReadOtherLink}</Link>{t.installPage.globalReadOtherB}
        </p>
      </section>

      <section id="structure" className="mb-12 scroll-mt-16">
        <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
          {t.installPage.structureTitle}
        </h2>
        <p className="text-base text-muted-foreground mb-6">
          {t.installPage.structureP}
        </p>

        <pre className="p-4 rounded-lg bg-code overflow-x-auto mb-4 text-sm font-mono text-code-foreground">
{`.agents/
├── agent/           # 20 Specialist Agents
├── skills/          # 48 Skills
├── workflows/       # 13 Slash Commands
├── rules/           # Workspace Rules
└── ARCHITECTURE.md  # Full documentation`}
        </pre>

        <div className="space-y-4">
          <div className="p-4 rounded-lg border border-border">
            <h3 className="font-semibold text-foreground mb-2">agent/</h3>
            <p className="text-sm text-muted-foreground">
              {t.installPage.agentDirDesc}
            </p>
          </div>
          <div className="p-4 rounded-lg border border-border">
            <h3 className="font-semibold text-foreground mb-2">skills/</h3>
            <p className="text-sm text-muted-foreground">
              {t.installPage.skillsDirDesc}
            </p>
          </div>
          <div className="p-4 rounded-lg border border-border">
            <h3 className="font-semibold text-foreground mb-2">workflows/</h3>
            <p className="text-sm text-muted-foreground">
              {t.installPage.workflowsDirDesc}
            </p>
          </div>
          <div className="p-4 rounded-lg border border-border">
            <h3 className="font-semibold text-foreground mb-2">rules/</h3>
            <p className="text-sm text-muted-foreground">
              {t.installPage.rulesDirDescA}<code className="px-1 py-0.5 rounded bg-muted font-mono text-xs">rules/*.md</code>{t.installPage.rulesDirDescB}
            </p>
          </div>
        </div>
      </section>

      <section id="requirements" className="mb-12 scroll-mt-16">
        <h2 className="text-2xl font-bold tracking-tight text-foreground mb-4">
          {t.installPage.requirementsTitle}
        </h2>
        <ul className="space-y-2 text-base text-muted-foreground mb-6">
          <li className="flex items-start gap-2">
            <svg className="w-5 h-5 text-green-600 dark:text-green-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span>{t.installPage.req1}</span>
          </li>
          <li className="flex items-start gap-2">
            <svg className="w-5 h-5 text-green-600 dark:text-green-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span>{t.installPage.req2}</span>
          </li>
          <li className="flex items-start gap-2">
            <svg className="w-5 h-5 text-green-600 dark:text-green-500 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span>{t.installPage.req3}</span>
          </li>
        </ul>
      </section>

      

      
    </div>
  );
}
