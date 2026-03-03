import { TextScramble } from "@/components/ui/text-scramble";

export default function TextScrambleDemo() {
    return (
        <main className="min-h-screen flex flex-col items-center justify-center gap-20 bg-background px-6">
            <div className="text-center space-y-3">
                <p className="text-[10px] uppercase tracking-[0.4em] text-muted-foreground font-mono">Hover to decode</p>
            </div>

            <div className="flex flex-col items-center gap-12">
                <TextScramble text="VIEW WORK" />
            </div>

            <p className="text-xs text-muted-foreground font-mono tracking-wide">[ kinetic typography ]</p>
        </main>
    )
}
