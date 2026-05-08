'use client';

import { useState } from 'react';
import { CheckIcon, CopyIcon } from 'lucide-react';

interface CodeBlockProps {
    code: string;
    language?: string;
    showLineNumbers?: boolean;
    className?: string;
}

export function CodeBlock({ code, language = 'bash', showLineNumbers = false, className }: CodeBlockProps) {
    const [copied, setCopied] = useState(false);

    const copyToClipboard = async () => {
        await navigator.clipboard.writeText(code);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className={`relative group ${className}`}>
            <pre className={`p-4 rounded-lg bg-zinc-900 dark:bg-zinc-900 overflow-x-auto border border-zinc-800 font-mono text-sm ${showLineNumbers ? 'pl-12' : ''}`}>
                <code className="text-zinc-100" data-language={language}>{code}</code>
            </pre>
            <button
                onClick={copyToClipboard}
                className="absolute top-3 right-3 p-2 rounded-md bg-zinc-800 hover:bg-zinc-700 transition-colors opacity-0 group-hover:opacity-100"
                aria-label="Copy code"
            >
                {copied ? (
                    <CheckIcon className="w-4 h-4 text-green-400" />
                ) : (
                    <CopyIcon className="w-4 h-4 text-zinc-400" />
                )}
            </button>
        </div>
    );
}
