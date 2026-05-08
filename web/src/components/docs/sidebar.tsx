'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navSections = [
    {
        title: 'Getting Started',
        items: [
            { href: '/docs', label: 'Introduction' },
            { href: '/docs/installation', label: 'Installation' },
        ],
    },
    {
        title: 'Core Concepts',
        items: [
            { href: '/docs/agents', label: 'Agents' },
            { href: '/docs/skills', label: 'Skills' },
            { href: '/docs/workflows', label: 'Workflows' },
        ],
    },
    {
        title: 'Guide',
        items: [
            { href: '/docs/guide/examples/brainstorm', label: 'Structured Brainstorming' },
            { href: '/docs/guide/examples/plan', label: 'Project Planning' },
            { href: '/docs/guide/examples/create', label: 'Create New Application' },
            { href: '/docs/guide/examples/new-feature', label: 'Add a New Feature' },
            { href: '/docs/guide/examples/ui-design', label: 'Advanced UI Design' },
            { href: '/docs/guide/examples/debugging', label: 'Systematic Debugging' },
            { href: '/docs/guide/examples/test', label: 'Test Generation' },
            { href: '/docs/guide/examples/preview', label: 'Preview Management' },
            { href: '/docs/guide/examples/status', label: 'Project Status' },
            { href: '/docs/guide/examples/orchestration', label: 'Multi-Agent Orchestration' },
            { href: '/docs/guide/examples/deployment', label: 'Production Deployment' },
        ],
    },
    {
        title: 'CLI Reference',
        items: [
            { href: '/docs/cli', label: 'Commands & Options' },
        ],
    },
];

export default function DocsSidebar() {
    const pathname = usePathname();

    return (
        <nav className="space-y-1">
            {navSections.map((section) => (
                <div key={section.title} className="pb-6">
                    <h3 className="mb-3 px-2 text-sm font-semibold text-zinc-900 dark:text-zinc-50">
                        {section.title}
                    </h3>
                    <div className="space-y-0.5">
                        {section.items.map((item) => {
                            const isActive = pathname === item.href;
                            return (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className={`
                    block px-2 py-1.5 text-sm rounded-md transition-colors
                    ${isActive
                                            ? 'bg-zinc-100 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-50 font-medium'
                                            : 'text-zinc-700 dark:text-zinc-300 hover:text-zinc-900 dark:hover:text-zinc-50 hover:bg-zinc-100 dark:hover:bg-zinc-800'
                                        }
                  `}
                                >
                                    {item.label}
                                </Link>
                            );
                        })}
                    </div>
                </div>
            ))}
        </nav>
    );
}
