// Shared wrapper: all standard pages use this to get padding + scroll
// The layout no longer provides overflow-y-auto or padding
export function PageShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex-1 overflow-y-auto p-8">
      {children}
    </div>
  )
}
