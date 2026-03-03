import './globals.css'
import type { Metadata } from 'next'
import { Lora, Raleway } from 'next/font/google'
import { Providers } from './providers'
import { Sidebar } from '@/components/Sidebar'

const lora = Lora({
  subsets: ['latin'],
  variable: '--font-lora',
  weight: ['400', '500', '600', '700']
})
const raleway = Raleway({
  subsets: ['latin'],
  variable: '--font-raleway',
  weight: ['300', '400', '500', '600', '700']
})

export const metadata: Metadata = {
  title: 'LUNA OS — Haven Escovaria & Esmalteria',
  description: 'Sistema de Atendimento IA para Haven Escovaria & Esmalteria. Dashboard de conversas, analytics, knowledge base e campanhas.',
  icons: {
    icon: '/favicon.ico',
  },
  other: {
    'theme-color': '#ec4899',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body className={`${raleway.className} ${lora.variable} ${raleway.variable}`}>
        <Providers>
          <div className="flex h-screen bg-[var(--color-bg)] transition-colors duration-500 font-sans">
            <Sidebar />
            <main className="flex-1 overflow-hidden flex flex-col p-6">
              {children}
            </main>
          </div>
        </Providers>
      </body>
    </html>
  )
}
