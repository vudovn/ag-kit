"use client";

import useSWR from 'swr'
import { motion, AnimatePresence } from 'framer-motion'
import {
  MessageSquare,
  TrendingUp,
  Calendar,
  Bot,
  Zap,
  ArrowUpRight,
  ArrowDownRight,
  Activity,
  Users,
  ShieldCheck,
  Brain,
  Swords,
  Lightbulb,
  BarChart3,
  CheckCircle2,
} from 'lucide-react'
import Link from 'next/link'
import { memo, useMemo } from 'react'
import type { DashboardData, SentimentData, MaturityData, KPICardProps } from '@/types'

const fetcher = (url: string) => fetch(url).then(res => res.json())

const KPICard = memo(({
  title,
  value,
  sub,
  icon: Icon,
  accent,
  trend,
  href,
  index
}: KPICardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
    >
      <Link href={href || '#'}>
        <div className="bg-white/80 backdrop-blur-md rounded-3xl p-6 border border-white/20 shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-all group relative overflow-hidden">
          <div className="flex items-start justify-between mb-4 relative z-10">
            <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${accent} shadow-sm group-hover:scale-110 transition-transform`}>
              <Icon className="w-6 h-6" />
            </div>
            {trend && (
              <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-[10px] font-black uppercase tracking-tighter ${trend === 'up' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'}`}>
                {trend === 'up' ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
                {trend === 'up' ? 'High' : 'Low'}
              </div>
            )}
          </div>
          <div className="relative z-10">
            <p className="text-xs text-gray-600 font-bold uppercase tracking-widest">{title}</p>
            <p className="text-4xl font-black text-gray-900 mt-2 tabular-nums">
              {value}
            </p>
            {sub && <p className="text-[10px] text-gray-600 font-medium mt-1 uppercase">{sub}</p>}
          </div>
          {/* Subtle background glow */}
          <div className={`absolute -right-4 -bottom-4 w-24 h-24 rounded-full opacity-0 group-hover:opacity-10 transition-opacity blur-3xl ${accent.split(' ')[0]}`} />
        </div>
      </Link>
    </motion.div>
  )
})
KPICard.displayName = 'KPICard'

export default function Dashboard() {
  // Optimized SWR configurations to reduce unnecessary re-renders
  const { data, error, isLoading } = useSWR<DashboardData>('/api/analytics/dashboard?days=7', fetcher, {
    refreshInterval: 60000, // Increased from 30s to 60s
    revalidateOnFocus: false, // Disabled to prevent unnecessary refreshes
    dedupingInterval: 10000,
    revalidateIfStale: true
  })

  const { data: maturityData } = useSWR('/api/evolution/maturity', fetcher, {
    refreshInterval: 30000, // Increased from 10s to 30s
    dedupingInterval: 10000
  })

  const { data: sentimentData } = useSWR<SentimentData>('/api/analytics/sentiment?days=7', fetcher, {
    refreshInterval: 120000, // Increased from 60s to 120s
    dedupingInterval: 10000
  })

  // Memoized calculations
  const avgResponseSec = useMemo(() =>
    Math.round((data?.messages?.avg_response_time_ms ?? 0) / 1000),
    [data?.messages?.avg_response_time_ms]
  )

  const totalSentiment = useMemo(() =>
    (sentimentData?.distribution?.positive ?? 0) +
    (sentimentData?.distribution?.negative ?? 0) +
    (sentimentData?.distribution?.neutral ?? 0),
    [sentimentData?.distribution]
  )

  const satisfactionPct = useMemo(() =>
    totalSentiment > 0
      ? ((sentimentData?.distribution?.positive ?? 0) / totalSentiment * 100).toFixed(1)
      : null,
    [sentimentData?.distribution?.positive, totalSentiment]
  )

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-[var(--color-bg)] transition-colors duration-500">
      <div className="max-w-7xl mx-auto space-y-10">

        {/* Page Header */}
        <div className="flex items-end justify-between">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <div className="flex items-center gap-2 mb-2">
              <span className="h-px w-8 bg-luna_pink-500" />
              <p className="text-[10px] font-black uppercase tracking-[0.2em] text-luna_pink-500">MCT Intelligence Protocol</p>
            </div>
            <h1 className="text-5xl font-black text-gray-950 tracking-tighter">Central de Comando</h1>
            <p className="text-gray-600 mt-2 text-sm font-medium flex items-center gap-2">
              Fluxo em tempo real · <span className="text-luna_pink-500">{(data?.period_days ?? 7)} dias de dados</span>
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex items-center gap-3 bg-white border border-gray-100 shadow-sm p-2 pr-5 rounded-2xl"
          >
            <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center">
              <Brain className="w-5 h-5 text-white animate-pulse" />
            </div>
            <div>
              <p className="text-[10px] font-black text-gray-600 uppercase tracking-widest">Luna Maturity</p>
              <p className="text-xs font-bold text-indigo-600 uppercase">{maturityData?.score || 0}% Ready</p>
            </div>
          </motion.div>
        </div>

        {/* KPI Grid */}
        <AnimatePresence mode="wait">
          {isLoading ? (
            <motion.div
              key="loading"
              exit={{ opacity: 0 }}
              className="grid grid-cols-2 lg:grid-cols-4 gap-6"
            >
              {[1, 2, 3, 4, 5].map(i => (
                <div key={i} className="h-44 bg-gray-100 rounded-[2rem] animate-pulse border border-gray-200" />
              ))}
            </motion.div>
          ) : (
            <div className="grid grid-cols-2 lg:grid-cols-5 gap-6">
              <KPICard
                index={0}
                title="Maturidade Sōra"
                value={`${maturityData?.score || 0}%`}
                sub="Combined Elite Score"
                icon={ShieldCheck}
                accent="bg-indigo-50 text-indigo-600 shadow-indigo-100"
                trend={maturityData?.score > 75 ? 'up' : null}
                href="/intelligence"
              />
              <KPICard
                index={1}
                title="Conversas Totais"
                value={data?.resumo?.total_conversas ?? data?.conversations?.total ?? 0}
                sub="Interações registradas"
                icon={MessageSquare}
                accent="bg-white text-gray-600"
                trend="up"
                href="/conversations"
              />
              <KPICard
                index={2}
                title="Conversão Real"
                value={`${data?.conversao?.taxa_conversao?.toFixed(1) ?? data?.conversations?.conversion_rate?.toFixed(1) ?? '0.0'}%`}
                sub={`${data?.conversao?.fechadas ?? data?.conversations?.converted ?? 0} Agendamentos`}
                icon={TrendingUp}
                accent="bg-emerald-50 text-emerald-600"
                trend="up"
              />
              <KPICard
                index={3}
                title="Carga de Agenda"
                value={data?.appointments?.total ?? 0}
                sub="Próximos compromissos"
                icon={Calendar}
                accent="bg-violet-50 text-violet-600"
              />
              <KPICard
                index={4}
                title="Latência IA"
                value={`${avgResponseSec}s`}
                sub="Resposta Média"
                icon={Zap}
                accent={avgResponseSec < 5 ? "bg-amber-50 text-amber-600" : "bg-red-50 text-red-600"}
              />
            </div>
          )}
        </AnimatePresence>

        {/* Intelligence Layer */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="lg:col-span-2 bg-gray-950 rounded-[2.5rem] shadow-2xl p-10 text-white relative overflow-hidden group"
          >
            {/* Background Decorative Element */}
            <div className="absolute top-0 right-0 w-96 h-96 bg-luna_pink-600/10 blur-[100px] -mr-48 -mt-48 transition-all group-hover:bg-luna_pink-600/20" />

            <div className="relative z-10">
              <div className="flex items-center justify-between mb-10">
                <div className="flex items-center gap-4">
                  <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-luna_pink-500 to-luna_pink-700 flex items-center justify-center shadow-lg shadow-luna_pink-900/50">
                    <Activity className="w-7 h-7 text-white" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-black tracking-tight">Vigilância Cognitiva</h2>
                    <p className="text-gray-300 text-sm font-medium">Métricas de performance da agente Luna</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-2 rounded-2xl">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                  <span className="text-[10px] font-black uppercase tracking-widest text-white">Live Monitoring</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white/5 backdrop-blur-sm rounded-3xl p-6 border border-white/10 hover:border-white/30 transition-all">
                  <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Taxa de Abandono</p>
                  <p className="text-4xl font-black text-red-400">{(((data?.conversao?.perdidas ?? 0) / (data?.conversations?.total || 1)) * 100).toFixed(1)}%</p>
                  <p className="text-[10px] text-gray-300 mt-2 font-bold uppercase">{data?.conversao?.perdidas ?? 0} Sessões perdidas</p>
                </div>
                <div className="bg-white/5 backdrop-blur-sm rounded-3xl p-6 border border-white/10 hover:border-white/30 transition-all">
                  <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Satisfação Geral</p>
                  <p className="text-4xl font-black text-emerald-400">{satisfactionPct ? <>{satisfactionPct}<span className="text-lg">%</span></> : <span className="text-gray-400">—</span>}</p>
                  <p className="text-[10px] text-gray-300 mt-2 font-bold uppercase">{satisfactionPct ? 'Baseado em NLP Context' : 'Sem dados suficientes'}</p>
                </div>
                <div className="bg-white/5 backdrop-blur-sm rounded-3xl p-6 border border-white/10 hover:border-white/30 transition-all">
                  <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Horas Poupadas</p>
                  <p className="text-4xl font-black text-purple-400">{data?.resumo?.human_hours_saved ?? 0}<span className="text-lg">h</span></p>
                  <p className="text-[10px] text-gray-300 mt-2 font-bold uppercase">Trabalho Humano Poupado</p>
                </div>
              </div>

              <div className="mt-10 flex items-center justify-between">
                <Link href="/conversations" className="group/btn flex items-center gap-3 bg-white text-gray-950 px-8 py-4 rounded-2xl font-black text-sm transition-transform hover:scale-105 active:scale-95">
                  Audit Channel History
                  <ArrowUpRight className="w-5 h-5 group-hover/btn:translate-x-1 group-hover/btn:-translate-y-1 transition-transform" />
                </Link>
                <div className="hidden md:block text-right">
                  <p className="text-[10px] font-black text-gray-600 uppercase tracking-[0.3em]">Sovereign Node</p>
                  <p className="text-xs font-bold text-gray-400 italic">v2.0-ELITE-REF</p>
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="flex flex-col gap-6"
          >
            <div className="flex-1 bg-white rounded-[2.5rem] border border-gray-100 shadow-sm p-10 relative overflow-hidden">
              <h2 className="text-xl font-black text-gray-900 mb-8 flex items-center gap-2">
                <CheckCircle2 className="w-6 h-6 text-luna_pink-500" />
                Ações Diretas
              </h2>

              <div className="space-y-4">
                {[
                  { label: 'Dojo Arena (Ollama)', href: '/dojo', icon: Swords, color: 'text-rose-600 bg-rose-50' },
                  { label: 'Super Analytics (30d)', href: '/analytics-super', icon: BarChart3, color: 'text-blue-600 bg-blue-50' },
                  { label: 'Configurar Personas', href: '/persona', icon: Users, color: 'text-violet-600 bg-violet-50' },
                  { label: 'Dossiês de Inteligência', href: '/intelligence', icon: Lightbulb, color: 'text-amber-600 bg-amber-50' },
                  { label: 'Histórico de Conversas', href: '/conversations', icon: MessageSquare, color: 'text-indigo-600 bg-indigo-50' },
                  { label: 'Base de Conhecimento', href: '/knowledge', icon: Brain, color: 'text-emerald-600 bg-emerald-50' },
                ].map(action => (
                  <Link
                    key={action.href}
                    href={action.href}
                    className="flex items-center gap-4 p-4 rounded-3xl hover:bg-gray-50 transition-all group border border-transparent hover:border-gray-100"
                  >
                    <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${action.color} transition-transform group-hover:rotate-6 shadow-sm`}>
                      <action.icon className="w-6 h-6" />
                    </div>
                    <span className="font-bold text-gray-700 group-hover:text-gray-950">{action.label}</span>
                    <div className="ml-auto w-8 h-8 rounded-lg bg-gray-50 flex items-center justify-center group-hover:bg-white border border-transparent group-hover:border-gray-200 transition-all">
                      <ArrowUpRight className="w-4 h-4 text-gray-300 group-hover:text-gray-900" />
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </motion.div>

        </div>
      </div>
    </div>
  )
}
