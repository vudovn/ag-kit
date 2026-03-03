"use client";

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion } from 'framer-motion'
import {
  LayoutDashboard,
  MessageSquare,
  BarChart3,
  Users,
  Megaphone,
  Brain,
  UserCircle2,
  Wifi,
  Settings,
  Swords,
  Lightbulb,
  Smartphone,
  TrendingUp,
  Scissors,
  Package,
} from 'lucide-react'

const mainNav = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Conversas', href: '/conversations', icon: MessageSquare, badge: 'LIVE' },
  { name: 'Analytics', href: '/analytics-super', icon: BarChart3, badge: 'PRO' },
  { name: 'Clientes', href: '/clients', icon: Users },
  { name: 'Campanhas', href: '/campaigns', icon: Megaphone },
  { name: 'Dojo Arena', href: '/dojo', icon: Swords },
  { name: 'Brain', href: '/brain', icon: Brain },
  { name: 'Intelligence', href: '/intelligence', icon: Lightbulb },
  { name: 'Persona', href: '/persona', icon: UserCircle2 },
]

const catalogNav = [
  { name: 'Serviços', href: '/services', icon: Scissors },
  { name: 'Profissionais', href: '/professionals', icon: Users },
  { name: 'Pacotes', href: '/packages', icon: Package },
]

const systemNav = [
  { name: 'Configurações', href: '/settings', icon: Settings },
]



function NavItem({ href, icon: Icon, name, badge }: { href: string; icon: any; name: string; badge?: string }) {
  const pathname = usePathname()
  const active = pathname === href

  return (
    <Link
      href={href}
      className={`
        group flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-semibold
        transition-all duration-300 relative overflow-hidden
        ${active
          ? 'bg-grad-premium text-white shadow-premium ring-1 ring-white/20'
          : 'text-gray-500 hover:bg-primary/5 hover:text-primary'
        }
      `}
    >
      <Icon className={`w-5 h-5 flex-shrink-0 transition-transform duration-300 group-hover:scale-110 ${active ? 'text-white' : 'text-primary/70'}`} />
      <span className="truncate">{name}</span>
      {badge && (
        <span className="ml-auto px-2 py-0.5 bg-gradient-to-r from-luna_pink-500 to-cta-DEFAULT text-white text-[9px] font-black uppercase tracking-wider rounded-full shadow-lg shadow-cta-DEFAULT/30">
          {badge}
        </span>
      )}
      {active && (
        <motion.div
          layoutId="sidebar-active"
          className="ml-auto w-1.5 h-1.5 rounded-full bg-white shadow-[0_0_8px_white]"
        />
      )}
    </Link>
  )
}

export function Sidebar() {
  return (
    <aside className="w-64 flex-shrink-0 flex flex-col bg-white/80 backdrop-blur-xl border-r border-white/50 shadow-2xl h-screen relative z-50">
      {/* Glow Effect */}
      <div className="absolute top-0 left-0 w-full h-32 bg-primary/5 blur-3xl -z-10" />

      {/* Logo */}
      <div className="px-6 py-8">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-grad-premium flex items-center justify-center shadow-lg border border-white/20">
            <span className="text-white font-black text-lg italic">L</span>
          </div>
          <div>
            <p className="font-black text-gray-900 text-base leading-none tracking-tighter">LUNA OS</p>
            <p className="text-[10px] text-luna_pink-500 font-bold mt-1 uppercase tracking-widest bg-luna_pink-50 px-1.5 py-0.5 rounded-md inline-block">Haven Soberana</p>
          </div>
        </div>
      </div>

      {/* Main Nav */}
      <nav className="flex-1 px-4 py-2 overflow-y-auto space-y-1 custom-scrollbar">
        <div className="px-4 mb-4 mt-2">
          <p className="section-label">Inteligência Operacional</p>
        </div>
        {mainNav.map(item => <NavItem key={item.href} {...item} />)}

        <div className="my-6 px-4">
          <div className="h-px bg-gradient-to-r from-transparent via-luna_pink-100 to-transparent" />
        </div>

        <div className="px-4 mb-4">
          <p className="section-label">Catálogo Haven</p>
        </div>
        {catalogNav.map(item => <NavItem key={item.href} {...item} />)}

        <div className="my-6 px-4">
          <div className="h-px bg-gradient-to-r from-transparent via-luna_pink-100 to-transparent" />
        </div>

        <div className="px-4 mb-4">
          <p className="section-label">Configuração Soberana</p>
        </div>
        {systemNav.map(item => <NavItem key={item.href} {...item} />)}
      </nav>

      {/* Footer status */}
      <div className="p-4 m-4 rounded-2xl bg-grad-soft border border-luna_pink-100 shadow-inner">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-3 h-3 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]" />
            <div className="absolute inset-0 w-3 h-3 rounded-full bg-emerald-400 animate-ping opacity-75" />
          </div>
          <div>
            <span className="block text-[11px] text-gray-900 font-black uppercase tracking-tight">Cérebro Luna v2.0</span>
            <span className="block text-[9px] text-luna_pink-400 font-bold">Protocolo Sync Ativo</span>
          </div>
        </div>
      </div>
    </aside>
  )
}
