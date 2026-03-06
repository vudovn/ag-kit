"use client";

import useSWR from 'swr';
import { motion } from 'framer-motion';
import type { ReactElement, ReactNode } from 'react';
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  Users,
  MessageSquare,
  Calendar,
  Clock,
  Target,
  AlertTriangle,
  CheckCircle,
  Activity,
  BarChart3,
  PieChart,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react';

const fetcher = (url: string) => fetch(url).then(res => res.json());

// ==================== Types ====================

interface KPICardProps {
  title: string
  value: string | number
  sub?: string
  icon: React.ElementType
  trend?: 'up' | 'down'
  color: string
  delay?: number
}

interface Gatilho {
  id: string
  tipo: string
  descricao: string
  prioridade: 'alta' | 'media' | 'baixa'
  timestamp: string
  mensagem?: string
  acao?: string
}

interface GatilhosCardProps {
  gatilhos: Gatilho[]
}

interface Funil {
  etapa: string
  valor: number
  cor: string
  nome?: string
  count?: number
}

interface FunilTaxa {
  [key: string]: number
}

interface FunilCardProps {
  funil: {
    etapas: Funil[]
    taxas?: FunilTaxa
  }
}

interface Tendencias {
  insights: Array<{
    id: string
    tipo: 'oportunidade' | 'atencao' | 'sucesso'
    descricao: string
    impacto: number
  }>
  tendencia?: string | { crescimento_percentual: number }
  projecao?: string | { proximos_7_dias: number; confianca: number }
}

interface TendenciasCardProps {
  tendencias: Tendencias
}

// ==================== COMPONENTES ====================

function KPICard({ title, value, sub, icon: Icon, trend, color, delay = 0 }: KPICardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5 }}
    >
      <div className="bg-white/90 backdrop-blur-xl rounded-3xl p-6 border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.06)] hover:shadow-[0_8px_30px_rgb(0,0,0,0.12)] transition-all group relative overflow-hidden">
        {/* Background gradient */}
        <div className={`absolute -right-8 -top-8 w-32 h-32 rounded-full opacity-10 group-hover:opacity-20 transition-opacity blur-3xl ${color}`} />
        
        {/* Content */}
        <div className="relative z-10">
          <div className="flex items-start justify-between mb-4">
            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center ${color} bg-opacity-10 group-hover:scale-110 transition-transform`}>
              <Icon className="w-7 h-7" />
            </div>
            
            {trend && (
              <div className={`flex items-center gap-1 px-3 py-1.5 rounded-full text-[10px] font-black uppercase tracking-tighter ${
                trend === 'up' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'
              }`}>
                {trend === 'up' ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
                {trend === 'up' ? 'High' : 'Low'}
              </div>
            )}
          </div>
          
          <div>
            <p className="text-xs text-gray-500 font-bold uppercase tracking-widest">{title}</p>
            <p className="text-4xl font-black text-gray-900 mt-2 tabular-nums tracking-tight">
              {value}
            </p>
            {sub && (
              <p className="text-[10px] text-gray-400 font-medium mt-2 uppercase tracking-wide">
                {sub}
              </p>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

function GatilhosCard({ gatilhos }: GatilhosCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.6 }}
      className="bg-white/90 backdrop-blur-xl rounded-3xl p-6 border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.06)]"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="w-12 h-12 rounded-2xl bg-orange-500 bg-opacity-10 flex items-center justify-center">
          <AlertTriangle className="w-6 h-6 text-orange-500" />
        </div>
        <div>
          <h3 className="font-bold text-gray-900 text-lg">Gatilhos Detectados</h3>
          <p className="text-xs text-gray-500 uppercase tracking-wide">{gatilhos.length} alertas</p>
        </div>
      </div>

      <div className="space-y-3">
        {gatilhos.map((gatilho: Gatilho, i: number) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.8 + i * 0.1 }}
            className={`p-4 rounded-2xl border-l-4 ${
              gatilho.prioridade === 'alta' ? 'bg-red-50 border-red-500' :
              gatilho.prioridade === 'media' ? 'bg-yellow-50 border-yellow-500' :
              'bg-blue-50 border-blue-500'
            }`}
          >
            <div className="flex items-start gap-3">
              <div className={`w-2 h-2 rounded-full mt-2 ${
                gatilho.prioridade === 'alta' ? 'bg-red-500' :
                gatilho.prioridade === 'media' ? 'bg-yellow-500' :
                'bg-blue-500'
              }`} />
              <div className="flex-1">
                <p className="font-semibold text-gray-900 text-sm">{gatilho.mensagem}</p>
                <p className="text-xs text-gray-600 mt-1">{gatilho.acao}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}

function FunilCard({ funil }: FunilCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.4 }}
      className="bg-white/90 backdrop-blur-xl rounded-3xl p-6 border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.06)]"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="w-12 h-12 rounded-2xl bg-purple-500 bg-opacity-10 flex items-center justify-center">
          <BarChart3 className="w-6 h-6 text-purple-500" />
        </div>
        <div>
          <h3 className="font-bold text-gray-900 text-lg">Funil de Conversão</h3>
          <p className="text-xs text-gray-500 uppercase tracking-wide">Jornada do cliente</p>
        </div>
      </div>

      <div className="space-y-4">
        {funil?.etapas?.map((etapa: Funil, i: number) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6 + i * 0.1 }}
            className="relative"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">{etapa.nome}</span>
              <span className="text-sm font-bold text-gray-900">{etapa.count}</span>
            </div>
            <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${funil.taxas?.[etapa.nome || ''] || 0}%` }}
                transition={{ delay: 0.8 + i * 0.1, duration: 0.5 }}
                className={`h-full rounded-full ${
                  i === 0 ? 'bg-blue-500' :
                  i === 1 ? 'bg-purple-500' :
                  i === 2 ? 'bg-pink-500' :
                  i === 3 ? 'bg-orange-500' :
                  'bg-green-500'
                }`}
              />
            </div>
            <div className="flex justify-end mt-1">
              <span className="text-[10px] text-gray-500 font-medium">
                {funil.taxas?.[etapa.nome || '']?.toFixed(1)}% da total
              </span>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}

function TendenciasCard({ tendencias }: TendenciasCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.8 }}
      className="bg-white/90 backdrop-blur-xl rounded-3xl p-6 border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.06)]"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="w-12 h-12 rounded-2xl bg-blue-500 bg-opacity-10 flex items-center justify-center">
          <Activity className="w-6 h-6 text-blue-500" />
        </div>
        <div>
          <h3 className="font-bold text-gray-900 text-lg">Tendências</h3>
          <p className="text-xs text-gray-500 uppercase tracking-wide">Projeções</p>
        </div>
      </div>
      
      <div className="space-y-4">
        <div className="flex items-center justify-between p-4 bg-green-50 rounded-2xl">
          <div className="flex items-center gap-3">
            <TrendingUp className="w-5 h-5 text-green-600" />
            <span className="text-sm font-medium text-gray-700">Crescimento</span>
          </div>
          <span className={`text-lg font-black ${
            typeof tendencias?.tendencia === 'object' && tendencias?.tendencia?.crescimento_percentual >= 0 ? 'text-green-600' : 'text-red-600'
          }`}>
            {typeof tendencias?.tendencia === 'object' ? tendencias?.tendencia?.crescimento_percentual?.toFixed(1) : '0'}%
          </span>
        </div>

        <div className="flex items-center justify-between p-4 bg-blue-50 rounded-2xl">
          <div className="flex items-center gap-3">
            <Target className="w-5 h-5 text-blue-600" />
            <span className="text-sm font-medium text-gray-700">Projeção (7 dias)</span>
          </div>
          <span className="text-lg font-black text-blue-600">
            {typeof tendencias?.projecao === 'object' ? tendencias?.projecao?.proximos_7_dias?.toFixed(0) : '0'}
          </span>
        </div>

        <div className="flex items-center justify-between p-4 bg-purple-50 rounded-2xl">
          <div className="flex items-center gap-3">
            <CheckCircle className="w-5 h-5 text-purple-600" />
            <span className="text-sm font-medium text-gray-700">Confiança</span>
          </div>
          <span className="text-sm font-black uppercase text-purple-600">
            {typeof tendencias?.projecao === 'object' ? tendencias?.projecao?.confianca : 'N/A'}
          </span>
        </div>
      </div>
    </motion.div>
  );
}

// ==================== MAIN COMPONENT ====================

export default function SuperAnalyticsDashboard() {
  // Optimized SWR with caching and staggered refresh
  const { data: overview, error: overviewError } = useSWR('/api/analytics/overview?days=30', fetcher, {
    refreshInterval: 60000,
    dedupingInterval: 30000,
    keepPreviousData: true,
    revalidateOnFocus: false
  });
  const { data: funil, error: funilError } = useSWR('/api/analytics/funil?days=30', fetcher, {
    refreshInterval: 60000,
    dedupingInterval: 30000,
    keepPreviousData: true,
    revalidateOnFocus: false
  });
  const { data: tendencias, error: tendenciasError } = useSWR('/api/analytics/tendencias?days=30', fetcher, {
    refreshInterval: 120000,
    dedupingInterval: 60000,
    keepPreviousData: true,
    revalidateOnFocus: false
  });
  const { data: gatilhos, error: gatilhosError } = useSWR('/api/analytics/gatilhos', fetcher, {
    refreshInterval: 30000,
    dedupingInterval: 15000,
    keepPreviousData: true,
    revalidateOnFocus: false
  });

  const isLoading = !overview || !funil || !tendencias || !gatilhos;

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-500 font-medium">Carregando analytics...</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-black text-gray-900 mb-2">Super Analytics</h1>
          <p className="text-gray-600">Análise rica com 20+ métricas avançadas</p>
        </motion.div>
        
        {/* KPIs */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <KPICard
            title="Total Conversas"
            value={overview?.resumo?.total_conversas || 0}
            sub={`${overview?.resumo?.media_mensagens_por_conversa?.toFixed(1)} msgs/conversa`}
            icon={MessageSquare}
            trend={overview?.resumo?.total_conversas > 100 ? 'up' : 'down'}
            color="bg-blue-500"
            delay={0}
          />
          
          <KPICard
            title="Receita Total"
            value={`R$ ${(overview?.financeiro?.receita_total || 0).toFixed(0)}`}
            sub={`Ticket: R$ ${(overview?.financeiro?.ticket_medio || 0).toFixed(0)}`}
            icon={DollarSign}
            trend="up"
            color="bg-green-500"
            delay={0.1}
          />
          
          <KPICard
            title="Clientes Ativos"
            value={overview?.financeiro?.clientes_ativos || 0}
            sub={`${overview?.resumo?.total_clientes || 0} total`}
            icon={Users}
            trend="up"
            color="bg-purple-500"
            delay={0.2}
          />
          
          <KPICard
            title="Taxa de Conversão"
            value={`${(overview?.conversao?.taxa_conversao || 0).toFixed(1)}%`}
            sub={`${overview?.conversao?.fechadas || 0} fechadas`}
            icon={Target}
            trend={(overview?.conversao?.taxa_conversao || 0) > 30 ? 'up' : 'down'}
            color="bg-orange-500"
            delay={0.3}
          />
        </div>
        
        {/* Cards Principais */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <GatilhosCard gatilhos={gatilhos?.gatilhos || []} />
          <FunilCard funil={funil?.funil} />
        </div>
        
        {/* Tendências e Insights */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <TendenciasCard tendencias={tendencias} />
          
          {/* Insights */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 1 }}
            className="bg-white/90 backdrop-blur-xl rounded-3xl p-6 border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.06)]"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-2xl bg-pink-500 bg-opacity-10 flex items-center justify-center">
                <PieChart className="w-6 h-6 text-pink-500" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900 text-lg">Insights</h3>
                <p className="text-xs text-gray-500 uppercase tracking-wide">Ações recomendadas</p>
              </div>
            </div>
            
            <div className="space-y-3">
              {overview?.insights?.map((insight: any, i: number) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 1.2 + i * 0.1 }}
                  className="p-4 bg-pink-50 rounded-2xl border-l-4 border-pink-500"
                >
                  <p className="font-semibold text-gray-900 text-sm">{insight.mensagem}</p>
                  <p className="text-xs text-gray-600 mt-1">{insight.acao}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
