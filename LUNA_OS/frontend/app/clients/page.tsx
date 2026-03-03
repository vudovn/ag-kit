"use client";

import { useState, useMemo } from 'react'
import useSWR from 'swr'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Users,
  Search,
  MessageSquare,
  Calendar,
  Phone,
  Loader2,
  Star,
  Clock,
  ArrowRight,
  Filter,
  Zap,
  TrendingUp,
  Activity,
  MoreVertical,
  Mail,
  MapPin,
  DollarSign,
  Sparkles,
  Bell,
  CheckCircle2,
  AlertCircle
} from 'lucide-react'

// Generic fetcher for SWR
const fetcher = (url: string) => fetch(url).then(r => r.json())

interface Client {
  id: string
  name?: string
  phone: string
  tags?: string[]
  last_contact?: string
  conversation_count?: number
  total_visits?: number
  total_spent?: number
  status?: 'active' | 'inactive' | 'vip'
  avatar_color?: string
}

interface Conversation {
  id: string
  started_at: string
  messages_count: number
  intent?: string
  sentiment?: string
}

interface ClientDetail extends Client {
  conversations?: Conversation[]
  recent_activity?: any[]
}

function timeAgo(iso: string) {
  if (!iso) return '—'
  const date = new Date(iso)
  const now = new Date()
  const diffInMs = now.getTime() - date.getTime()
  const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24))

  if (diffInDays === 0) return 'Hoje'
  if (diffInDays === 1) return 'Ontem'
  if (diffInDays < 7) return `${diffInDays}d atrás`
  return date.toLocaleDateString('pt-BR')
}

function getStatusBadge(client: Client) {
  if (client.tags?.includes('vip')) {
    return (
      <span className="inline-flex items-center gap-1 bg-gradient-to-r from-amber-500 to-orange-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-lg shadow-amber-500/30">
        <Star className="w-2.5 h-2.5 fill-current" /> VIP
      </span>
    )
  }
  
  const days = client.last_contact ? 
    Math.floor((new Date().getTime() - new Date(client.last_contact).getTime()) / (1000 * 60 * 60 * 24)) 
    : 999
  
  if (days <= 3) {
    return (
      <span className="inline-flex items-center gap-1 bg-green-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">
        <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse" /> Ativo
      </span>
    )
  }
  
  if (days <= 30) {
    return (
      <span className="inline-flex items-center gap-1 bg-blue-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">
        Recente
      </span>
    )
  }
  
  return (
    <span className="inline-flex items-center gap-1 bg-gray-400 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">
      Inativo
    </span>
  )
}

const AVATAR_COLORS = [
  'from-pink-500 to-rose-500',
  'from-purple-500 to-indigo-500',
  'from-cyan-500 to-blue-500',
  'from-emerald-500 to-teal-500',
  'from-orange-500 to-amber-500',
  'from-red-500 to-pink-500',
]

function getAvatarColor(index: number) {
  return AVATAR_COLORS[index % AVATAR_COLORS.length]
}

// Skeleton Loader Component
function ClientListSkeleton() {
  return (
    <div className="space-y-3 p-4">
      {[...Array(6)].map((_, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: i * 0.1 }}
          className="flex items-center gap-4 p-4 rounded-2xl bg-gray-50"
        >
          <div className="w-12 h-12 rounded-full bg-gray-200 animate-pulse" />
          <div className="flex-1 space-y-2">
            <div className="h-4 bg-gray-200 rounded w-3/4 animate-pulse" />
            <div className="h-3 bg-gray-200 rounded w-1/2 animate-pulse" />
          </div>
          <div className="w-16 h-8 bg-gray-200 rounded animate-pulse" />
        </motion.div>
      ))}
    </div>
  )
}

// Stats Card Component
function StatsCard({ icon: Icon, label, value, trend, color }: any) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm"
    >
      <div className="flex items-center justify-between">
        <div className={`w-10 h-10 rounded-xl bg-${color}-50 flex items-center justify-center`}>
          <Icon className={`w-5 h-5 text-${color}-500`} />
        </div>
        {trend && (
          <span className={`text-xs font-bold ${trend > 0 ? 'text-green-500' : 'text-red-500'}`}>
            {trend > 0 ? '+' : ''}{trend}%
          </span>
        )}
      </div>
      <div className="mt-3">
        <p className="text-2xl font-black text-gray-900">{value}</p>
        <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mt-1">{label}</p>
      </div>
    </motion.div>
  )
}

export default function ClientsPage() {
  const [search, setSearch] = useState('')
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [filter, setFilter] = useState<'all' | 'active' | 'vip' | 'inactive'>('all')

  const { data: clientsData, error: clientsError, isLoading: clientsLoading } = useSWR<Client[]>('/api/clients', fetcher, {
    refreshInterval: 30000
  })

  const { data: detailData, isLoading: detailLoading } = useSWR<ClientDetail>(
    selectedId ? `/api/clients/${selectedId}` : null,
    fetcher
  )

  const clients = Array.isArray(clientsData) ? clientsData : []

  const filtered = useMemo(() => {
    return clients.filter(c => {
      // Search filter
      const matchesSearch = !search || 
        c.name?.toLowerCase().includes(search.toLowerCase()) || 
        c.phone?.includes(search)
      
      // Status filter
      let matchesFilter = true
      if (filter === 'vip') matchesFilter = c.tags?.includes('vip') ?? false
      if (filter === 'active') {
        const days = c.last_contact ?
          Math.floor((new Date().getTime() - new Date(c.last_contact).getTime()) / (1000 * 60 * 60 * 24))
          : 999
        matchesFilter = days <= 7
      }
      if (filter === 'inactive') {
        const days = c.last_contact ?
          Math.floor((new Date().getTime() - new Date(c.last_contact).getTime()) / (1000 * 60 * 60 * 24))
          : 0
        matchesFilter = days > 30
      }
      
      return matchesSearch && matchesFilter
    })
  }, [clients, search, filter])

  const selectedClient = useMemo(() => {
    return clients.find(c => c.id === selectedId)
  }, [clients, selectedId])

  // Calculate stats
  const stats = useMemo(() => {
    const total = clients.length
    const vip = clients.filter(c => c.tags?.includes('vip')).length
    const active = clients.filter(c => {
      const days = c.last_contact ? 
        Math.floor((new Date().getTime() - new Date(c.last_contact).getTime()) / (1000 * 60 * 60 * 24)) 
        : 999
      return days <= 7
    }).length
    const totalSpent = clients.reduce((sum, c) => sum + (c.total_spent || 0), 0)
    
    return { total, vip, active, totalSpent }
  }, [clients])

  return (
    <div className="flex flex-col h-[calc(100vh-120px)] gap-6">
      {/* Header Soberano */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-black text-gray-900 tracking-tight flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center shadow-lg shadow-primary/30">
              <Users className="w-5 h-5 text-white" />
            </div>
            Base de Inteligência
          </h1>
          <p className="text-gray-500 mt-2 text-sm font-medium flex items-center gap-2">
            <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            Gestão unificada de perfis e interações WhatsApp
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden md:flex flex-col items-end px-5 py-3 bg-gradient-to-br from-primary/10 to-purple-500/10 rounded-2xl border border-primary/20">
            <span className="text-[9px] font-bold text-gray-500 uppercase tracking-widest">Total Sincronizado</span>
            <span className="text-2xl font-black text-primary">{clients.length}</span>
          </div>
          <button className="bg-gray-900 text-white px-5 py-3 rounded-2xl font-bold flex items-center gap-2 hover:bg-gray-800 transition-all shadow-lg hover:shadow-xl active:scale-95">
            <Filter className="w-4 h-4" />
            <span>Filtros</span>
          </button>
        </div>
      </motion.div>

      {/* Stats Row */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-4 gap-4"
      >
        <StatsCard
          icon={Users}
          label="Total Clientes"
          value={stats.total}
          trend={12}
          color="blue"
        />
        <StatsCard
          icon={Star}
          label="Clientes VIP"
          value={stats.vip}
          trend={8}
          color="amber"
        />
        <StatsCard
          icon={Activity}
          label="Ativos (7d)"
          value={stats.active}
          trend={-3}
          color="green"
        />
        <StatsCard
          icon={DollarSign}
          label="Receita Total"
          value={`R$ ${(stats.totalSpent / 1000).toFixed(1)}k`}
          trend={25}
          color="purple"
        />
      </motion.div>

      <div className="flex flex-1 gap-6 min-h-0">
        {/* Lado Esquerdo: Listagem */}
        <div className="w-1/3 flex flex-col bg-white rounded-3xl border border-gray-200 shadow-xl overflow-hidden">
          {/* Search & Filter */}
          <div className="p-5 border-b border-gray-100 bg-gradient-to-b from-white to-gray-50/50">
            <div className="relative group mb-4">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-focus-within:text-primary transition-colors" />
              <input
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Buscar por nome ou telefone..."
                className="w-full pl-12 pr-4 py-3.5 bg-white border-2 border-gray-200 rounded-2xl text-sm font-medium focus:outline-none focus:ring-0 focus:border-primary transition-all shadow-sm"
              />
            </div>
            
            {/* Filter Tabs */}
            <div className="flex gap-2">
              {(['all', 'active', 'vip', 'inactive'] as const).map((f) => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`flex-1 py-2 px-3 rounded-xl text-xs font-bold transition-all ${
                    filter === f
                      ? 'bg-primary text-white shadow-md shadow-primary/30'
                      : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                  }`}
                >
                  {f === 'all' && 'Todos'}
                  {f === 'active' && 'Ativos'}
                  {f === 'vip' && 'VIP'}
                  {f === 'inactive' && 'Inativos'}
                </button>
              ))}
            </div>
          </div>

          {/* Client List */}
          <div className="flex-1 overflow-y-auto custom-scrollbar">
            {clientsLoading ? (
              <ClientListSkeleton />
            ) : filtered.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full py-16 text-center px-6">
                <div className="w-20 h-20 bg-gray-50 rounded-3xl flex items-center justify-center mb-6">
                  <Search className="w-8 h-8 text-gray-300" />
                </div>
                <p className="text-gray-900 font-bold text-lg">Nenhum cliente encontrado</p>
                <p className="text-sm text-gray-500 mt-2 max-w-[250px]">
                  {search ? 'Tente buscar por outro termo' : 'Aguarde novas mensagens do WhatsApp'}
                </p>
              </div>
            ) : (
              <div className="p-4 space-y-2">
                <AnimatePresence initial={false}>
                  {filtered.map((client, idx) => (
                    <motion.button
                      key={client.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.03 }}
                      onClick={() => setSelectedId(client.id)}
                      className={`w-full text-left p-4 rounded-2xl transition-all relative group ${
                        selectedId === client.id
                          ? 'bg-gradient-to-br from-primary to-primary-dark text-white shadow-xl shadow-primary/30 ring-2 ring-white/50'
                          : 'hover:bg-gray-50 border border-transparent hover:border-gray-200'
                      }`}
                    >
                      <div className="flex items-center gap-4">
                        {/* Avatar */}
                        <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${client.avatar_color || getAvatarColor(idx)} flex items-center justify-center text-xl font-black text-white shadow-lg transition-transform group-hover:scale-105`}>
                          {client.name?.[0]?.toUpperCase() || '?'}
                        </div>

                        {/* Info */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <p className={`font-bold truncate ${selectedId === client.id ? 'text-white' : 'text-gray-900'}`}>
                              {client.name || 'Sem nome'}
                            </p>
                            {getStatusBadge(client)}
                          </div>
                          <div className="flex items-center gap-3">
                            <p className={`text-xs flex items-center gap-1.5 ${selectedId === client.id ? 'text-white/80' : 'text-gray-500'}`}>
                              <Phone className="w-3 h-3" /> {client.phone}
                            </p>
                            {client.conversation_count && client.conversation_count > 10 && (
                              <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${selectedId === client.id ? 'bg-white/20 text-white' : 'bg-amber-100 text-amber-700'}`}>
                                📞 {client.conversation_count}
                              </span>
                            )}
                          </div>
                        </div>

                        {/* Time */}
                        <div className="text-right">
                          <p className={`text-[10px] font-bold uppercase tracking-tighter ${selectedId === client.id ? 'text-white/70' : 'text-gray-400'}`}>
                            {timeAgo(client.last_contact || '')}
                          </p>
                          <ArrowRight className={`w-4 h-4 mt-1 transition-all ${selectedId === client.id ? 'text-white' : 'text-gray-300 opacity-0 group-hover:opacity-100 group-hover:translate-x-1'}`} />
                        </div>
                      </div>
                    </motion.button>
                  ))}
                </AnimatePresence>
              </div>
            )}
          </div>

          {/* List Footer */}
          <div className="p-4 border-t border-gray-100 bg-gray-50/50">
            <p className="text-xs font-bold text-gray-400 text-center">
              {filtered.length} de {clients.length} clientes exibidos
            </p>
          </div>
        </div>

        {/* Lado Direito: Dashboard do Cliente */}
        <div className="flex-1 bg-white rounded-3xl border border-gray-200 shadow-xl overflow-hidden flex flex-col relative">
          <AnimatePresence mode="wait">
            {!selectedId ? (
              <motion.div
                key="empty"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 1.05 }}
                className="flex-1 flex flex-col items-center justify-center text-center p-12 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50"
              >
                <motion.div
                  animate={{ 
                    y: [0, -10, 0],
                    rotate: [0, 5, -5, 0]
                  }}
                  transition={{ 
                    duration: 3,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                  className="w-28 h-28 bg-white rounded-3xl shadow-2xl flex items-center justify-center mb-8"
                >
                  <Users className="w-14 h-14 text-primary/30" />
                </motion.div>
                <h3 className="text-2xl font-black text-gray-900 mb-3">Selecione um Cliente</h3>
                <p className="text-gray-500 max-w-md leading-relaxed">
                  Explore o histórico completo de conversas, analyze tendências de comportamento e visualize insights de inteligência artificial.
                </p>
                
                {/* Quick Stats */}
                <div className="grid grid-cols-3 gap-4 mt-10">
                  <div className="bg-white/80 backdrop-blur-sm p-4 rounded-2xl border border-white/50 shadow-lg">
                    <Users className="w-6 h-6 text-blue-500 mx-auto mb-2" />
                    <p className="text-2xl font-black text-gray-900">{stats.total}</p>
                    <p className="text-xs font-bold text-gray-400">Total</p>
                  </div>
                  <div className="bg-white/80 backdrop-blur-sm p-4 rounded-2xl border border-white/50 shadow-lg">
                    <Star className="w-6 h-6 text-amber-500 mx-auto mb-2" />
                    <p className="text-2xl font-black text-gray-900">{stats.vip}</p>
                    <p className="text-xs font-bold text-gray-400">VIPs</p>
                  </div>
                  <div className="bg-white/80 backdrop-blur-sm p-4 rounded-2xl border border-white/50 shadow-lg">
                    <Activity className="w-6 h-6 text-green-500 mx-auto mb-2" />
                    <p className="text-2xl font-black text-gray-900">{stats.active}</p>
                    <p className="text-xs font-bold text-gray-400">Ativos</p>
                  </div>
                </div>
              </motion.div>
            ) : (
              <motion.div
                key={selectedId}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, scale: 0.98 }}
                className="flex-1 flex flex-col min-h-0"
              >
                {/* Perfil Header */}
                <div className="p-8 bg-gradient-to-r from-primary via-purple-600 to-pink-600 text-white relative overflow-hidden">
                  {/* Background Pattern */}
                  <div className="absolute inset-0 opacity-10">
                    <div className="absolute top-10 left-10 w-32 h-32 bg-white rounded-full blur-3xl" />
                    <div className="absolute bottom-10 right-10 w-40 h-40 bg-white rounded-full blur-3xl" />
                  </div>

                  <div className="flex items-center gap-6 relative z-10">
                    <div className="w-28 h-28 rounded-3xl bg-white/20 backdrop-blur-md border-2 border-white/30 p-1 shadow-2xl">
                      <div className={`w-full h-full rounded-2xl bg-gradient-to-br ${selectedClient?.avatar_color || 'from-primary to-purple-600'} text-white flex items-center justify-center text-4xl font-black`}>
                        {selectedClient?.name?.[0]?.toUpperCase() || '?'}
                      </div>
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h2 className="text-3xl font-black tracking-tight">{selectedClient?.name || 'Cliente Sem Nome'}</h2>
                        {selectedClient && getStatusBadge(selectedClient)}
                      </div>
                      <div className="flex items-center gap-3 flex-wrap">
                        <div className="flex items-center gap-2 bg-white/15 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-bold border border-white/20">
                          <Phone className="w-4 h-4" /> {selectedClient?.phone}
                        </div>
                        <div className="flex items-center gap-2 bg-white/15 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-bold border border-white/20">
                          <MessageSquare className="w-4 h-4" /> {selectedClient?.conversation_count || 0} conversas
                        </div>
                        <div className="flex items-center gap-2 bg-white/15 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-bold border border-white/20">
                          <Calendar className="w-4 h-4" /> {timeAgo(selectedClient?.last_contact || '')}
                        </div>
                      </div>
                    </div>
                    
                    {/* Actions */}
                    <div className="flex items-center gap-2">
                      <button className="w-12 h-12 rounded-2xl bg-white/20 backdrop-blur-sm border border-white/30 flex items-center justify-center hover:bg-white/30 transition-all">
                        <MoreVertical className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-8 custom-scrollbar">
                  {/* KPIs */}
                  <div className="grid grid-cols-3 gap-5 mb-8">
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.1 }}
                      className="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-3xl border border-blue-100 shadow-sm group hover:shadow-lg transition-all"
                    >
                      <div className="flex items-center gap-3 mb-3">
                        <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center shadow-md group-hover:scale-110 transition-transform">
                          <MessageSquare className="w-6 h-6 text-blue-500" />
                        </div>
                        <TrendingUp className="w-5 h-5 text-green-500" />
                      </div>
                      <p className="text-3xl font-black text-gray-900">{selectedClient?.conversation_count || 0}</p>
                      <p className="text-xs font-bold text-gray-500 uppercase tracking-widest mt-1">Interações Totais</p>
                    </motion.div>

                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.2 }}
                      className="bg-gradient-to-br from-purple-50 to-pink-50 p-6 rounded-3xl border border-purple-100 shadow-sm group hover:shadow-lg transition-all"
                    >
                      <div className="flex items-center gap-3 mb-3">
                        <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center shadow-md group-hover:scale-110 transition-transform">
                          <Calendar className="w-6 h-6 text-purple-500" />
                        </div>
                        <CheckCircle2 className="w-5 h-5 text-green-500" />
                      </div>
                      <p className="text-3xl font-black text-gray-900">{selectedClient?.total_visits || 0}</p>
                      <p className="text-xs font-bold text-gray-500 uppercase tracking-widest mt-1">Visitas Realizadas</p>
                    </motion.div>

                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.3 }}
                      className="bg-gradient-to-br from-amber-50 to-orange-50 p-6 rounded-3xl border border-amber-100 shadow-sm group hover:shadow-lg transition-all"
                    >
                      <div className="flex items-center gap-3 mb-3">
                        <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center shadow-md group-hover:scale-110 transition-transform">
                          <DollarSign className="w-6 h-6 text-amber-500" />
                        </div>
                        <Sparkles className="w-5 h-5 text-amber-500" />
                      </div>
                      <p className="text-3xl font-black text-gray-900">
                        R$ {selectedClient?.total_spent ? (selectedClient.total_spent / (selectedClient.total_visits || 1)).toFixed(2) : '0.00'}
                      </p>
                      <p className="text-xs font-bold text-gray-500 uppercase tracking-widest mt-1">Ticket Médio</p>
                    </motion.div>
                  </div>

                  {/* Intelligence Section */}
                  <div className="bg-gradient-to-br from-gray-50 to-white rounded-3xl border border-gray-200 p-6 mb-6">
                    <div className="flex items-center justify-between mb-6">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-primary to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-primary/30">
                          <Zap className="w-5 h-5 text-white" />
                        </div>
                        <div>
                          <h4 className="font-black text-gray-900">Live Insight Engine</h4>
                          <p className="text-xs text-gray-500">Inteligência em tempo real</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2 bg-green-50 px-4 py-2 rounded-full border border-green-200">
                        <span className="w-2.5 h-2.5 bg-green-500 rounded-full animate-pulse" />
                        <span className="text-xs font-bold text-green-700">Sync Ativo</span>
                      </div>
                    </div>

                    {detailLoading ? (
                      <div className="flex items-center justify-center py-12">
                        <Loader2 className="w-8 h-8 animate-spin text-primary" />
                      </div>
                    ) : (
                      <div className="space-y-3">
                        {(!detailData?.conversations || detailData.conversations.length === 0) ? (
                          <div className="p-8 text-center bg-white rounded-2xl border-2 border-dashed border-gray-200">
                            <AlertCircle className="w-8 h-8 text-gray-300 mx-auto mb-3" />
                            <p className="text-gray-500 font-medium">Nenhuma conversa registrada</p>
                            <p className="text-xs text-gray-400 mt-1">As conversas aparecerão aqui conforme forem sincronizadas</p>
                          </div>
                        ) : (
                          <div className="space-y-2">
                            {detailData.conversations.slice(0, 5).map((conv: any) => (
                              <motion.div
                                key={conv.id}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm flex items-center justify-between hover:shadow-md hover:border-primary/30 transition-all cursor-pointer group"
                              >
                                <div className="flex items-center gap-4">
                                  <div className="w-10 h-10 bg-gradient-to-br from-primary/20 to-purple-500/20 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
                                    <MessageSquare className="w-5 h-5 text-primary" />
                                  </div>
                                  <div>
                                    <p className="text-sm font-bold text-gray-900">Protocolo #{conv.id.slice(0, 8)}</p>
                                    <p className="text-xs text-gray-400">{new Date(conv.started_at).toLocaleString()}</p>
                                  </div>
                                </div>
                                <div className="flex items-center gap-3">
                                  {conv.sentiment && (
                                    <span className={`text-[10px] font-bold px-2 py-1 rounded-full ${
                                      conv.sentiment === 'positive' ? 'bg-green-100 text-green-700' :
                                      conv.sentiment === 'negative' ? 'bg-red-100 text-red-700' :
                                      'bg-gray-100 text-gray-600'
                                    }`}>
                                      {conv.sentiment === 'positive' && '😊 '}
                                      {conv.sentiment === 'negative' && '😕 '}
                                      {conv.sentiment === 'neutral' && '😐 '}
                                      {conv.sentiment}
                                    </span>
                                  )}
                                  <span className="text-[10px] font-bold bg-primary/5 text-primary px-3 py-1.5 rounded-full uppercase tracking-wider">
                                    {conv.intent || 'Geral'}
                                  </span>
                                </div>
                              </motion.div>
                            ))}
                            <button className="w-full py-3 text-sm font-bold text-primary hover:bg-primary/5 rounded-xl transition-all flex items-center justify-center gap-2">
                              Ver histórico completo
                              <ArrowRight className="w-4 h-4" />
                            </button>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                {/* Footer Actions */}
                <div className="p-6 bg-white border-t border-gray-200 flex items-center justify-between gap-4">
                  <button className="text-sm font-bold text-gray-500 hover:text-gray-900 transition-colors flex items-center gap-2">
                    <Bell className="w-4 h-4" />
                    Criar lembrete
                  </button>
                  <div className="flex items-center gap-3">
                    <button className="px-5 py-3 bg-gray-100 border border-gray-200 rounded-2xl text-sm font-bold text-gray-700 hover:bg-gray-200 transition-all active:scale-95 flex items-center gap-2">
                      <Mail className="w-4 h-4" />
                      Enviar e-mail
                    </button>
                    <button className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-2xl text-sm font-bold hover:from-green-600 hover:to-emerald-700 transition-all shadow-lg shadow-green-500/30 active:scale-95 flex items-center gap-2">
                      <MessageSquare className="w-4 h-4" />
                      Enviar WhatsApp
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}
