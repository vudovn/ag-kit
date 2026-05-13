import Image from "next/image";
import Link from "next/link";
import { GithubIcon } from "lucide-react";
import Typing from "@/components/typing";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between bg-white px-8 py-24 dark:bg-black sm:items-start sm:px-16 sm:py-32">
        <Image
          src="/images/logo.png"
          alt="AG Kit logo"
          width={72}
          height={72}
          priority
          className="h-16 w-16"
        />

        <div className="flex flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
            <span className="before:-inset-x-1 before:-rotate-1 relative z-4 before:pointer-events-none before:absolute before:inset-y-0 before:z-4 before:bg-linear-to-r before:from-blue-500 before:via-cyan-500 before:to-orange-500 before:opacity-16 before:mix-blend-hard-light">
              AG Kit
            </span>
          </h1>
          <p className="max-w-md text-lg leading-8 text-zinc-600 dark:text-zinc-400">
            AI agent templates with Skills, Agents, and Workflows for modern
            coding assistants.
          </p>
          <Typing />
        </div>

        <div className="flex flex-col gap-4 text-base font-medium sm:flex-row">
          <a
            className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc] md:w-[158px]"
            href="https://github.com/vudovn/ag-kit"
            target="_blank"
            rel="noopener noreferrer"
          >
            <GithubIcon className="h-5 w-5" />
            GitHub
          </a>
          <Link
            className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc] md:w-[158px]"
            href="/docs"
          >
            Documentation
          </Link>
        </div>
      </main>
    </div>
  );
}
