'use client';

import { useTheme } from 'next-themes';
import { useSyncExternalStore } from 'react';
import { Button } from '../../../ui/button';

function subscribe() {
    return () => {};
}

function getClientSnapshot() {
    return true;
}

function getServerSnapshot() {
    return false;
}

export default function ThemeToggle() {
    const mounted = useSyncExternalStore(subscribe, getClientSnapshot, getServerSnapshot);
    const { theme, setTheme } = useTheme();

    if (!mounted) {
        return (
            <div className="w-9 h-9 rounded-md border border-zinc-200 dark:border-zinc-800" />
        );
    }

    return (
        <Button
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            variant="ghost"
            size="icon"
            aria-label="Toggle theme"
        >
            {theme === 'dark' ? (
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width={24}
                    height={24}
                    viewBox="0 0 24 24"
                    fill="none"
                    className="-rotate-45 size-4 text-zinc-700 dark:text-zinc-300"
                    strokeWidth={2}
                    stroke="currentColor"
                >
                    <path
                        d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z"
                        stroke="currentColor"
                        strokeWidth={2}
                    />
                    <path
                        d="M5 20L19 5"
                        stroke="currentColor"
                        strokeLinejoin="round"
                        strokeWidth={2}
                    />
                    <path
                        d="M16 9L22 13.8528M12.4128 12.4059L19.3601 18.3634M8 15.6672L15 21.5"
                        stroke="currentColor"
                        strokeLinejoin="round"
                        strokeWidth={2}
                    />
                </svg>
            ) : (
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width={24}
                    height={24}
                    viewBox="0 0 24 24"
                    fill="none"
                    className="-rotate-225 size-4 text-zinc-700 dark:text-zinc-300"
                    strokeWidth={2}
                    stroke="currentColor"
                >
                    <path
                        d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z"
                        stroke="currentColor"
                        strokeWidth={2}
                    />
                    <path
                        d="M5 20L19 5"
                        stroke="currentColor"
                        strokeLinejoin="round"
                        strokeWidth={2}
                    />
                    <path
                        d="M16 9L22 13.8528M12.4128 12.4059L19.3601 18.3634M8 15.6672L15 21.5"
                        stroke="currentColor"
                        strokeLinejoin="round"
                        strokeWidth={2}
                    />
                </svg>
            )}
        </Button>
    );
}
