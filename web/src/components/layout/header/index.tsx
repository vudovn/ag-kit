import Link from "next/link";
import MobileMenu from "@/components/layout/header/components/mobile-menu";
import SearchDialog from "@/components/layout/header/components/search-dialog";
import ThemeToggle from "@/components/layout/header/components/theme-toggle";
import DonateDialog from "@/components/layout/header/components/donate-dialog";
import { Button } from "@/components/ui/button";
import { GithubIcon } from "lucide-react";

const DiscordIcon = () => {
    return (
<svg
  viewBox="0 -28.5 256 256"
  version="1.1"
  xmlns="http://www.w3.org/2000/svg"
  xmlnsXlink="http://www.w3.org/1999/xlink"
  preserveAspectRatio="xMidYMid"
  fill="#000000"
>
  <g id="SVGRepo_bgCarrier" strokeWidth={0} />
  <g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round" />
  <g id="SVGRepo_iconCarrier">
    {" "}
    <g>
      {" "}
      <path
        d="M216.856339,16.5966031 C200.285002,8.84328665 182.566144,3.2084988 164.041564,0 C161.766523,4.11318106 159.108624,9.64549908 157.276099,14.0464379 C137.583995,11.0849896 118.072967,11.0849896 98.7430163,14.0464379 C96.9108417,9.64549908 94.1925838,4.11318106 91.8971895,0 C73.3526068,3.2084988 55.6133949,8.86399117 39.0420583,16.6376612 C5.61752293,67.146514 -3.4433191,116.400813 1.08711069,164.955721 C23.2560196,181.510915 44.7403634,191.567697 65.8621325,198.148576 C71.0772151,190.971126 75.7283628,183.341335 79.7352139,175.300261 C72.104019,172.400575 64.7949724,168.822202 57.8887866,164.667963 C59.7209612,163.310589 61.5131304,161.891452 63.2445898,160.431257 C105.36741,180.133187 151.134928,180.133187 192.754523,160.431257 C194.506336,161.891452 196.298154,163.310589 198.110326,164.667963 C191.183787,168.842556 183.854737,172.420929 176.223542,175.320965 C180.230393,183.341335 184.861538,190.991831 190.096624,198.16893 C211.238746,191.588051 232.743023,181.531619 254.911949,164.955721 C260.227747,108.668201 245.831087,59.8662432 216.856339,16.5966031 Z M85.4738752,135.09489 C72.8290281,135.09489 62.4592217,123.290155 62.4592217,108.914901 C62.4592217,94.5396472 72.607595,82.7145587 85.4738752,82.7145587 C98.3405064,82.7145587 108.709962,94.5189427 108.488529,108.914901 C108.508531,123.290155 98.3405064,135.09489 85.4738752,135.09489 Z M170.525237,135.09489 C157.88039,135.09489 147.510584,123.290155 147.510584,108.914901 C147.510584,94.5396472 157.658606,82.7145587 170.525237,82.7145587 C183.391518,82.7145587 193.761324,94.5189427 193.539891,108.914901 C193.539891,123.290155 183.391518,135.09489 170.525237,135.09489 Z"
        fill="#5865F2"
        fillRule="nonzero"
      >
        {" "}
      </path>{" "}
    </g>{" "}
  </g>
</svg>

    );
};

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
                                <span className="hidden sm:inline">AG Kit</span>
                                <span className="sm:hidden">AG Kit</span>
                            </Link>
                        </span>

                        {/* Separator */}
                        <div className="hidden sm:block w-px h-6 bg-zinc-200 dark:bg-zinc-800 shrink-0" />

                        {/* Desktop Nav */}
                        <nav className="hidden sm:flex items-center gap-1 flex-1 min-w-0">
                            <DonateDialog />
                            <Link href="https://github.com/vudovn/ag-kit" target="_blank" rel="noopener noreferrer">
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