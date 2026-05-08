import Link from "next/link";
import MobileMenu from "@/components/layout/header/components/mobile-menu";
import SearchDialog from "@/components/layout/header/components/search-dialog";
import ThemeToggle from "@/components/layout/header/components/theme-toggle";
import DonateDialog from "@/components/layout/header/components/donate-dialog";
import { Button } from "@/components/ui/button";
import { GithubIcon } from "lucide-react";

export default function Header() {
    return (
        <header className="sticky top-0 z-50 w-full border-b border-zinc-200 dark:border-zinc-800 bg-white/95 dark:bg-zinc-950/95 backdrop-blur supports-[backdrop-filter]:bg-white/80 supports-[backdrop-filter]:dark:bg-zinc-950/80">
            <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative">
                <div className="flex h-14 items-center justify-between gap-2 sm:gap-4">
                    {/* Left Section */}
                    <div className="flex items-center gap-2 sm:gap-3 md:gap-6 flex-1 min-w-0">
                        {/* Mobile Menu */}
                        <div className="lg:hidden">
                            <MobileMenu />
                        </div>

                        {/* Logo - Responsive */}
                        <span className="text-zinc-900 dark:text-white before:-inset-x-1 before:-rotate-1 relative z-4 before:pointer-events-none before:absolute before:inset-y-0 before:z-4 before:bg-linear-to-r before:from-blue-500 before:via-cyan-500 before:to-orange-500 before:opacity-16 before:mix-blend-hard-light font-semibold text-sm sm:text-base truncate">
                            <Link href="/" className="flex items-center gap-2 shrink-0 min-w-0">
                                <span className="hidden sm:inline">Antigravity Kit</span>
                                <span className="sm:hidden">AG Kit</span>
                            </Link>
                        </span>

                        {/* Separator */}
                        <div className="hidden sm:block w-px h-6 bg-zinc-200 dark:bg-zinc-800 shrink-0" />

                        {/* Desktop Nav */}
                        <nav className="hidden sm:flex items-center gap-1 flex-1 min-w-0">
                            <DonateDialog />
                            <Link href="https://github.com/vudovn/antigravity-kit" target="_blank" rel="noopener noreferrer">
                                <Button variant="outline" className="hidden md:flex">
                                    <GithubIcon className="w-4 h-4 mr-2" />
                                    GitHub
                                </Button>
                            </Link>
                            {/* <Link href="https://discord.gg/CwpvDdFK" target="_blank" rel="noopener noreferrer">
                                <Button variant="outline" className="hidden md:flex">
                                    <DiscordIcon />
                                    Discord
                                </Button>
                            </Link> */}
                            <Link href="https://unikorn.vn/" target="_blank" rel="noopener noreferrer">
                                <Button variant="outline" className="hidden md:flex">
                                    <svg
                                        width={24}
                                        height={24}
                                        viewBox="0 0 1000 1000"
                                        fill="currentColor"
                                        className="shrink-0"
                                        >
                                        <g transform="matrix(1,0,0,1,0,9.204355)">
                                            <path d="M890.828,5.864C895.373,4.486 900.302,5.343 904.116,8.172C907.93,11.002 910.178,15.47 910.178,20.219C910.178,143.585 910.178,795.144 910.178,961.372C910.178,967.476 906.48,972.971 900.825,975.269C895.17,977.566 888.687,976.208 884.429,971.834C645.13,726.029 399.028,922.802 198.646,716.77C128.914,644.809 89.922,548.538 89.922,448.334C89.822,333.557 89.822,156.891 89.822,111.128C89.822,104.519 94.147,98.689 100.472,96.773C147.714,82.457 338.731,24.573 400.472,5.864C405.016,4.486 409.945,5.343 413.759,8.172C417.573,11.002 419.822,15.47 419.822,20.219C419.822,92.456 419.822,340.356 419.822,469.822C419.822,514.103 455.719,550 500,550L500,550C544.281,550 580.178,514.103 580.178,469.822L580.178,111.128C580.178,104.519 584.504,98.689 590.828,96.773C638.071,82.457 829.088,24.573 890.828,5.864Z" />
                                        </g>
                                        </svg>
                                    Sponsored
                                </Button>
                            </Link>
                        </nav>
                    </div>

                    {/* Right Section */}
                    <div className="flex items-center gap-2 sm:gap-3 shrink-0">
                        {/* Search - Desktop */}
                        <div className="hidden md:block w-64">
                            <SearchDialog />
                        </div>

                        {/* Mobile Search Button */}
                        <div className="md:hidden">
                            <SearchDialog />
                        </div>

                        {/* Separator */}
                        <div className="hidden md:block w-px h-6 bg-zinc-200 dark:bg-zinc-800" />

                        {/* Theme Toggle */}
                        <ThemeToggle />
                    </div>
                </div>
            </div>
        </header>
    )
}
