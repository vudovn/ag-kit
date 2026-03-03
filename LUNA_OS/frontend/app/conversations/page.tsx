"use client";

import { useState, useRef, useEffect, useMemo } from 'react'
import useSWR from 'swr'
import { motion, AnimatePresence } from 'framer-motion'
import {
  MessageSquare,
  Target,
  Smile,
  AlertTriangle,
  Lightbulb,
  Clock,
  Search,
  CheckCircle,
  XCircle,
  Loader2,
  RefreshCw,
  Zap,
  User,
  Hash,
  Activity,
  ShieldCheck,
  ShieldAlert,
  ThumbsUp,
  ThumbsDown,
  AlertCircle,
  TrendingUp,
} from 'lucide-react'

interface Conversation {
  id: string
  client_name: string
  client_phone: string
  status: string
  intent?: string
  sentiment?: string
  started_at: string
  needs_human_intervention?: boolean
  handled_by?: string
  handoff_reason?: string
}

interface Message {
  id: string
  direction: 'inbound' | 'outbound'
  content: string
  created_at: string
  intent?: string
  intent_detected?: string
  sentiment?: string
  model_used?: string
  confidence_score?: number
  guardrail_passed?: boolean
  feedback?: string
  handled_by?: string
}

interface ConversationDetail extends Conversation {
  messages: Message[]
}

const fetcher = (url: string) => fetch(url).then(res => res.json())

function SentimentIcon({ sentiment }: { sentiment?: string }) {
  if (sentiment === 'positive') return <span title="Positivo">😊</span>
  if (sentiment === 'negative') return <span title="Negativo">😟</span>
  return <span title="Neutro">😐</span>
}

function timeAgo(iso: string) {
  if (!iso) return '—'
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 60000)
  if (diff < 1) return 'agora'
  if (diff < 60) return `${diff}m`
  if (diff < 1440) return `${Math.floor(diff / 60)}h`
  return `${Math.floor(diff / 1440)}d`
}

// ── Confidence Badge ──────────────────────────
function ConfidenceBadge({ score }: { score?: number }) {
  if (score == null) return null
  const pct = Math.round(score * 100)

  let color = 'bg-emerald-50 text-emerald-600 border-emerald-200'
  let label = 'Alta'
  let icon = <ShieldCheck className="w-3 h-3" />

  if (score < 0.60) {
    color = 'bg-red-50 text-red-600 border-red-200'
    label = 'Baixa'
    icon = <ShieldAlert className="w-3 h-3" />
  } else if (score < 0.85) {
    color = 'bg-amber-50 text-amber-600 border-amber-200'
    label = 'Média'
    icon = <AlertCircle className="w-3 h-3" />
  }

  return (
    <div className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[9px] font-black uppercase tracking-tight border ${color}`} title={`Confiança: ${pct}%`}>
      {icon}
      <span>{pct}%</span>
      <span className="hidden sm:inline">{label}</span>
    </div>
  )
}

// ── Feedback Buttons ──────────────────────────
function FeedbackButtons({
  messageId,
  currentFeedback,
  onFeedback
}: {
  messageId: string
  currentFeedback?: string
  onFeedback: (id: string, feedback: string) => void
}) {
  if (currentFeedback) {
    return (
      <div className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[9px] font-black uppercase ${currentFeedback === 'positive' ? 'bg-emerald-100 text-emerald-600' : 'bg-red-100 text-red-600'}`}>
        {currentFeedback === 'positive' ? <ThumbsUp className="w-3 h-3" /> : <ThumbsDown className="w-3 h-3" />}
        {currentFeedback === 'positive' ? 'Correto' : 'Corrigido'}
      </div>
    )
  }

  return (
    <div className="inline-flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
      <button
        onClick={(e) => { e.stopPropagation(); onFeedback(messageId, 'positive') }}
        className="p-1.5 rounded-xl bg-white border border-gray-100 text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 hover:border-emerald-200 transition-all shadow-sm"
        title="Resposta correta"
      >
        <ThumbsUp className="w-3.5 h-3.5" />
      </button>
      <button
        onClick={(e) => { e.stopPropagation(); onFeedback(messageId, 'negative') }}
        className="p-1.5 rounded-xl bg-white border border-gray-100 text-gray-400 hover:text-red-600 hover:bg-red-50 hover:border-red-200 transition-all shadow-sm"
        title="Resposta incorreta"
      >
        <ThumbsDown className="w-3.5 h-3.5" />
      </button>
    </div>
  )
}

// ── Toast/Notification Simple Component ─────────────────
function Toast({ message, type, onClose }: { message: string, type: 'success' | 'error' | 'info', onClose: () => void }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000)
    return () => clearTimeout(timer)
  }, [onClose])

  return (
    <motion.div
      initial={{ opacity: 0, y: 50, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9, y: 20 }}
      className={`fixed bottom-8 right-8 z-50 px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3 border backdrop-blur-md ${type === 'success' ? 'bg-emerald-500/90 text-white border-emerald-400' :
          type === 'error' ? 'bg-red-500/90 text-white border-red-400' :
            'bg-gray-900/90 text-white border-gray-800'
        }`}
    >
      {type === 'success' ? <CheckCircle className="w-5 h-5" /> : type === 'error' ? <AlertCircle className="w-5 h-5" /> : <Loader2 className="w-5 h-5 animate-spin" />}
      <span className="font-bold text-sm tracking-tight">{message}</span>
    </motion.div>
  )
}

export default function ConversationsPage() {
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)

  // UX States
  const [isTakingOver, setIsTakingOver] = useState(false)
  const [toast, setToast] = useState<{ msg: string, type: 'success' | 'error' | 'info' } | null>(null)

  // 1. Fetch Lists
  const { data: conversations = [], mutate: mutateList, isValidating: loadingConvs } = useSWR<Conversation[]>('/api/conversations', fetcher, {
    refreshInterval: 10000
  })

  // 2. Fetch Detail
  const { data: detail, mutate: mutateDetail, isValidating: loadingMsgs } = useSWR<ConversationDetail>(
    selectedId ? `/api/conversations/${selectedId}` : null,
    fetcher,
    { refreshInterval: 5000 }
  )

  const messages = detail?.messages || []

  useEffect(() => {
    if (messages.length > 0) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages.length])

  const filtered = useMemo(() => conversations.filter(c =>
    !search || c.client_name?.toLowerCase().includes(search.toLowerCase()) || c.client_phone?.includes(search)
  ), [conversations, search])

  // Insights logic
  const intentions = messages.map(m => m.intent || m.intent_detected).filter(Boolean) as string[]
  const topIntentMap = intentions.reduce((acc: Record<string, number>, i) => {
    acc[i] = (acc[i] || 0) + 1
    return acc
  }, {})
  const dominantIntent = Object.entries(topIntentMap).sort((a, b) => b[1] - a[1])[0]?.[0]
  const lastInbound = [...messages].reverse().find(m => m.direction === 'inbound')
  const negativeMsgCount = messages.filter(m => m.direction === 'inbound' && m.sentiment === 'negative').length
  const modelsUsed = Array.from(new Set(messages.map(m => m.model_used).filter(Boolean))) as string[]

  // [AUTOMELHORIA] Métricas de confiança da conversa
  const outboundMessages = messages.filter(m => m.direction === 'outbound')
  const scoredMessages = outboundMessages.filter(m => m.confidence_score != null)
  const avgConfidence = scoredMessages.length > 0
    ? scoredMessages.reduce((sum, m) => sum + (m.confidence_score || 0), 0) / scoredMessages.length
    : null
  const guardrailBlocks = outboundMessages.filter(m => m.guardrail_passed === false).length
  const feedbackCount = outboundMessages.filter(m => m.feedback != null).length

  // [AUTOMELHORIA] Handler de feedback
  const handleFeedback = async (messageId: string, feedback: string) => {
    try {
      await fetch('/api/conversations/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message_id: messageId, feedback }),
      })
      // Refresh messages
      mutateDetail()
    } catch (err) {
      console.error('Feedback error:', err)
      setToast({ msg: 'Erro ao enviar feedback', type: 'error' })
    }
  }

  // [UX] Action de Assumir Conversa / Human Handoff
  const handleTakeover = async () => {
    if (!selectedId) return
    setIsTakingOver(true)
    try {
      // Mock de Request de Handoff 
      // await fetch(`/api/conversations/${selectedId}/handoff`, { method: 'POST' })
      setToast({ msg: 'Atendimento Assumido! A IA foi pausada para esta conversa.', type: 'success' })
      mutateDetail()
      mutateList()
    } catch (error) {
      setToast({ msg: 'Falha ao processar intervenção.', type: 'error' })
    } finally {
      setIsTakingOver(false)
    }
  }

  return (
    <div className="flex-1 flex overflow-hidden bg-[#F9FBFF] p-6 gap-6 relative">
      <AnimatePresence>
        {toast && <Toast message={toast.msg} type={toast.type} onClose={() => setToast(null)} />}
      </AnimatePresence>

      {/* LEFT — List Panes */}
      <div className="w-80 flex flex-col bg-white rounded-[2rem] border border-gray-100 shadow-sm overflow-hidden flex-shrink-0">
        <div className="p-6 border-b border-gray-50 bg-white/50 backdrop-blur-sm sticky top-0 z-10">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h2 className="text-xl font-black text-gray-950 tracking-tight">Conversas</h2>
              <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">{filtered.length} Ativas</p>
            </div>
            <button
              onClick={() => mutateList()}
              className={`p-2 rounded-xl border border-gray-100 hover:bg-gray-50 group transition-all ${loadingConvs ? 'bg-gray-50' : ''}`}
            >
              <RefreshCw className={`w-4 h-4 text-gray-400 group-hover:text-luna-600 ${loadingConvs ? 'animate-spin' : ''}`} />
            </button>
          </div>
          <div className="relative group">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-300 group-focus-within:text-luna-500 transition-colors" />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Localizar contato..."
              className="w-full pl-11 pr-4 py-3 bg-gray-50/50 border border-gray-100 rounded-2xl text-sm font-medium focus:outline-none focus:ring-2 focus:ring-luna-500/20 focus:bg-white transition-all"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto px-2 py-4 space-y-2 custom-scrollbar">
          <AnimatePresence mode="popLayout">
            {filtered.map((conv, idx) => (
              <motion.button
                layout
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                key={conv.id}
                onClick={() => setSelectedId(conv.id)}
                className={`w-full text-left flex items-start gap-4 p-4 rounded-3xl transition-all group ${selectedId === conv.id ? 'bg-luna-600 text-white shadow-lg shadow-luna-200' : 'hover:bg-gray-50'}`}
              >
                <div className={`w-11 h-11 rounded-2xl font-black text-sm flex items-center justify-center flex-shrink-0 shadow-sm transition-transform group-hover:scale-105 ${selectedId === conv.id ? 'bg-white/20 text-white' : 'bg-luna-50 text-luna-600'}`}>
                  {conv.client_name?.[0]?.toUpperCase() || <User size={18} />}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between mb-0.5">
                    <p className={`font-bold text-sm truncate ${selectedId === conv.id ? 'text-white' : 'text-gray-900'}`}>{conv.client_name || conv.client_phone}</p>
                    <span className={`text-[9px] font-bold uppercase tracking-tighter ${selectedId === conv.id ? 'text-white/60' : 'text-gray-400'}`}>{timeAgo(conv.started_at)}</span>
                  </div>
                  <p className={`text-[10px] font-medium truncate ${selectedId === conv.id ? 'text-white/50' : 'text-gray-400'}`}>{conv.client_phone}</p>

                  <div className="flex items-center gap-2 mt-2">
                    <div className={`w-1.5 h-1.5 rounded-full ${conv.status === 'active' ? (selectedId === conv.id ? 'bg-white' : 'bg-green-500 animate-pulse') : (selectedId === conv.id ? 'bg-white/20' : 'bg-gray-300')}`} />
                    {conv.intent && (
                      <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded-full ${selectedId === conv.id ? 'bg-white/20 text-white' : 'bg-blue-50 text-blue-600'}`}>
                        {conv.intent}
                      </span>
                    )}
                    {conv.needs_human_intervention && (
                      <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded-full flex items-center gap-1 ${selectedId === conv.id ? 'bg-orange-500/20 text-orange-200 border border-orange-200/50' : 'bg-orange-50 text-orange-600 border border-orange-200'}`}>
                        <AlertTriangle className="w-2.5 h-2.5" /> Hand-off
                      </span>
                    )}
                  </div>
                </div>
              </motion.button>
            ))}
          </AnimatePresence>
        </div>
      </div>

      {/* CENTER — Intelligence View */}
      <div className="flex-1 flex flex-col bg-white rounded-[2rem] border border-gray-100 shadow-sm overflow-hidden min-w-0">
        <AnimatePresence mode="wait">
          {!selectedId ? (
            <motion.div
              key="empty"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex-1 flex flex-col items-center justify-center text-center p-12"
            >
              <div className="w-24 h-24 rounded-[2rem] bg-gray-50 flex items-center justify-center mb-6">
                <MessageSquare className="w-10 h-10 text-gray-200" />
              </div>
              <h3 className="text-xl font-black text-gray-400">Canal de Comunicação</h3>
              <p className="text-sm text-gray-300 max-w-xs mt-2">Selecione uma sessão para carregar o histórico e os insights da Luna.</p>
            </motion.div>
          ) : (
            <motion.div
              key="active"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex-1 flex flex-col min-h-0"
            >
              {/* Header */}
              <div className="px-8 py-6 border-b border-gray-50 flex items-center justify-between bg-white/50 backdrop-blur-sm">
                <div className="flex items-center gap-4">
                  <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center shadow-inner">
                    <span className="text-2xl font-black text-gray-400">{detail?.client_name?.[0] || <User size={24} />}</span>
                  </div>
                  <div>
                    <h3 className="text-xl font-black text-gray-950 tracking-tight">{detail?.client_name || detail?.client_phone}</h3>
                    <div className="flex items-center gap-2">
                      <Hash className="w-3 h-3 text-gray-300" />
                      <p className="text-xs font-bold text-gray-400">{detail?.client_phone}</p>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  {loadingMsgs && <Loader2 className="w-4 h-4 text-luna-500 animate-spin" />}
                  {avgConfidence != null && <ConfidenceBadge score={avgConfidence} />}
                  <div className={`flex items-center gap-2 px-4 py-2 rounded-2xl text-[10px] font-black uppercase tracking-widest border transition-all ${detail?.status === 'active' ? 'bg-emerald-50 text-emerald-600 border-emerald-100' : 'bg-gray-50 text-gray-400 border-gray-100'}`}>
                    {detail?.status === 'active' ? <><div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" /> Ativo</> : detail?.status}
                  </div>
                  {detail?.needs_human_intervention ? (
                    <button
                      onClick={handleTakeover}
                      disabled={isTakingOver}
                      className="flex items-center gap-2 px-4 py-2 bg-gray-950 text-white rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-gray-800 transition-colors shadow-lg shadow-gray-900/10 disabled:opacity-50"
                    >
                      {isTakingOver ? <Loader2 className="w-3 h-3 animate-spin" /> : null}
                      {isTakingOver ? 'Processando...' : 'Assumir Atendimento'}
                    </button>
                  ) : (
                    <button
                      onClick={handleTakeover}
                      disabled={isTakingOver}
                      className="flex items-center gap-2 px-4 py-2 bg-white text-gray-600 border border-gray-200 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-gray-50 transition-colors disabled:opacity-50"
                    >
                      {isTakingOver ? <Loader2 className="w-3 h-3 animate-spin" /> : null}
                      {isTakingOver ? 'Desligando IA...' : 'Intervir Manualmente'}
                    </button>
                  )}
                </div>
              </div>

              {/* Chat Body */}
              <div className="flex-1 overflow-y-auto p-8 space-y-6 custom-scrollbar bg-[#FAFAFC]">
                {detail?.needs_human_intervention && !detail?.handled_by && (
                  <div className="bg-orange-50 border border-orange-200 p-4 rounded-3xl flex items-start gap-4 shadow-sm mb-4">
                    <div className="w-10 h-10 rounded-2xl bg-orange-100 flex items-center justify-center flex-shrink-0">
                      <AlertTriangle className="w-5 h-5 text-orange-600" />
                    </div>
                    <div>
                      <h4 className="text-sm font-black text-orange-950 tracking-tight">IA Solicitou Intervenção Humana</h4>
                      <p className="text-xs font-medium text-orange-800 mt-1">A Luna não possui confiança suficiente para responder ou o cliente solicitou falar com um atendente humano. Clique em "Assumir Atendimento" no topo para pausar a IA.</p>
                      {detail.handoff_reason && (
                        <div className="mt-2 text-[10px] font-bold uppercase tracking-widest text-orange-600 bg-orange-100/50 inline-block px-3 py-1 rounded-lg border border-orange-200">
                          Motivo: {detail.handoff_reason}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                <AnimatePresence mode="popLayout">
                  {messages.length === 0 ? (
                    <div className="py-20 text-center"><p className="text-sm text-gray-300">Nenhum dado de mensagem no buffer</p></div>
                  ) : messages.map((msg, idx) => (
                    <motion.div
                      initial={{ opacity: 0, y: 10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      key={msg.id}
                      className={`flex ${msg.direction === 'outbound' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`max-w-[70%] group relative`}>
                        <div className={`rounded-3xl px-6 py-4 shadow-sm border ${msg.direction === 'outbound' ? 'bg-luna-900 border-luna-950 text-white rounded-tr-none' : 'bg-white border-gray-100 text-gray-800 rounded-tl-none'}`}>
                          <p className="text-sm leading-relaxed font-medium">{msg.content}</p>
                          <div className={`flex items-center gap-2 mt-2 pt-2 border-t flex-wrap ${msg.direction === 'outbound' ? 'border-white/10' : 'border-gray-50'}`}>
                            <span className={`text-[9px] font-bold uppercase tracking-widest ${msg.direction === 'outbound' ? 'text-white/40' : 'text-gray-300'}`}>
                              {new Date(msg.created_at).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
                            </span>
                            {msg.model_used && <span className={`text-[9px] font-black uppercase italic ${msg.direction === 'outbound' ? 'text-luna-400' : 'text-gray-400'}`}>{msg.model_used.split('/').pop()}</span>}
                            {msg.sentiment && <SentimentIcon sentiment={msg.sentiment} />}

                            {/* [AUTOMELHORIA] Confidence Badge */}
                            {msg.direction === 'outbound' && msg.confidence_score != null && (
                              <ConfidenceBadge score={msg.confidence_score} />
                            )}

                            {/* [AUTOMELHORIA] Guardrail Shield */}
                            {msg.direction === 'outbound' && msg.guardrail_passed === false && (
                              <div className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[9px] font-black uppercase bg-orange-50 text-orange-600 border border-orange-200" title="Guardrails ativados nesta resposta">
                                <ShieldAlert className="w-3 h-3" />
                                Protegida
                              </div>
                            )}
                          </div>
                        </div>

                        {/* Meta info floating — intent badge */}
                        {(msg.intent || msg.intent_detected) && msg.direction === 'inbound' && (
                          <div className="absolute top-0 right-0 -mr-2 -mt-2 bg-blue-600 text-white text-[8px] font-black px-2 py-1 rounded-lg uppercase shadow-lg">
                            {msg.intent || msg.intent_detected}
                          </div>
                        )}

                        {/* [AUTOMELHORIA] Feedback Buttons — só para outbound */}
                        {msg.direction === 'outbound' && (
                          <div className="mt-2 flex justify-end">
                            <FeedbackButtons
                              messageId={msg.id}
                              currentFeedback={msg.feedback}
                              onFeedback={handleFeedback}
                            />
                          </div>
                        )}
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
                <div ref={bottomRef} />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* RIGHT — Intelligence Sidebar */}
      <div className="w-72 flex-shrink-0 flex flex-col gap-6">

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-gray-950 rounded-[2.5rem] p-8 text-white shadow-2xl relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-40 h-40 bg-luna-600/20 blur-[60px] -mr-20 -mt-20" />
          <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-500 mb-6 flex items-center gap-2">
            <Activity className="w-3 h-3" /> Live Intelligence
          </h3>

          {!selectedId ? (
            <div className="py-10 text-center"><p className="text-xs text-gray-600 italic">Waiting for session...</p></div>
          ) : (
            <div className="space-y-6 relative z-10">
              <div className="bg-white/5 rounded-3xl p-5 border border-white/10 transition-colors hover:border-white/30">
                <p className="text-[9px] font-black text-luna-400 uppercase tracking-widest mb-1">Objetivo Híbrido</p>
                <div className="flex items-center gap-2">
                  <Target className="w-4 h-4 text-white" />
                  <p className="text-sm font-black capitalize tracking-tight">{dominantIntent || 'Navegação'}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/5 rounded-2xl p-4 border border-white/10">
                  <p className="text-[8px] font-black text-gray-500 uppercase mb-1">Sentimento</p>
                  <p className="text-sm font-black">{lastInbound?.sentiment === 'positive' ? 'Vibrant' : lastInbound?.sentiment === 'negative' ? 'Critical' : 'Stable'}</p>
                </div>
                <div className="bg-white/5 rounded-2xl p-4 border border-white/10">
                  <p className="text-[8px] font-black text-gray-500 uppercase mb-1">Objeções</p>
                  <p className="text-sm font-black text-red-400">{negativeMsgCount}</p>
                </div>
              </div>

              {/* [AUTOMELHORIA] Métricas de Confiança */}
              <div className="pt-4 border-t border-white/10 space-y-4">
                <p className="text-[9px] font-black text-luna-400 uppercase tracking-widest">Automelhoria</p>

                <div className="bg-white/5 rounded-2xl p-4 border border-white/10">
                  <p className="text-[8px] font-black text-gray-500 uppercase mb-1">Confiança Média</p>
                  <div className="flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-emerald-400" />
                    <p className="text-lg font-black">
                      {avgConfidence != null ? `${Math.round(avgConfidence * 100)}%` : '—'}
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-white/5 rounded-2xl p-3 border border-white/10">
                    <p className="text-[8px] font-black text-gray-500 uppercase mb-1">Guardrails</p>
                    <p className={`text-sm font-black ${guardrailBlocks > 0 ? 'text-orange-400' : 'text-emerald-400'}`}>
                      {guardrailBlocks > 0 ? `${guardrailBlocks} ativados` : '✓ Limpo'}
                    </p>
                  </div>
                  <div className="bg-white/5 rounded-2xl p-3 border border-white/10">
                    <p className="text-[8px] font-black text-gray-500 uppercase mb-1">Feedback</p>
                    <p className="text-sm font-black text-blue-400">{feedbackCount} dado(s)</p>
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-white/10 space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-[9px] font-bold text-gray-500 uppercase tracking-widest">Model Stack</span>
                  <div className="flex -space-x-2">
                    {modelsUsed.map(m => (
                      <div key={m} className="w-6 h-6 rounded-lg bg-luna-600 border-2 border-gray-950 flex items-center justify-center text-[8px] font-black" title={m}>
                        {m[0].toUpperCase()}
                      </div>
                    ))}
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-[9px] font-bold text-gray-500 uppercase tracking-widest">Message Log</span>
                  <span className="text-sm font-black text-white">{messages.length}</span>
                </div>
              </div>
            </div>
          )}
        </motion.div>

        <div className="bg-white rounded-[2rem] border border-gray-100 p-8 shadow-sm group">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-2xl bg-amber-50 flex items-center justify-center">
              <Lightbulb className="w-5 h-5 text-amber-500" />
            </div>
            <h3 className="font-black text-gray-900 tracking-tight">AI Hints</h3>
          </div>
          <div className="space-y-3">
            <div className="p-3 bg-gray-50 rounded-2xl border-l-4 border-l-luna-500">
              <p className="text-[11px] font-medium text-gray-600">Luna está priorizando agendamentos para o turno da manhã conforme regra de ocupação.</p>
            </div>
            {guardrailBlocks > 0 && (
              <div className="p-3 bg-orange-50 rounded-2xl border-l-4 border-l-orange-500">
                <p className="text-[11px] font-medium text-orange-700">⚠️ {guardrailBlocks} resposta(s) foram corrigidas pelos Guardrails nesta conversa.</p>
              </div>
            )}
            <div className="p-3 bg-gray-50 rounded-2xl border-l-4 border-l-purple-500">
              <p className="text-[11px] font-medium text-gray-600">Use 👍/👎 nas respostas para ajudar a Luna a aprender.</p>
            </div>
          </div>
        </div>

        <div className="mt-auto bg-gradient-to-br from-indigo-600 to-purple-700 rounded-3xl p-6 text-white shadow-xl shadow-indigo-100 flex items-center justify-between">
          <div>
            <p className="text-[10px] font-black uppercase tracking-widest text-white/60 mb-1">MCT Sync Engine</p>
            <p className="text-lg font-black tracking-tight">Active</p>
          </div>
          <Zap className="w-8 h-8 text-white/20" />
        </div>

      </div>
    </div>
  )
}
