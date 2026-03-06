"use client";

import { useState, useEffect, useCallback, useRef, useMemo } from 'react'
import {
  Brain, Search, Plus, Trash2, Edit2, Check, X,
  BookOpen, MessageSquare, Lightbulb, Target, Building2,
  Loader2, ChevronDown, ChevronUp, Database, Sparkles, Save, Wand2,
  Send, Bot, User, Clock, Zap, RefreshCw, AlertCircle, CheckCircle
} from 'lucide-react'
import { memo } from 'react'
import type { KnowledgeItem, KnowledgeCategory } from '@/types'

// Settings Status
type SaveStatus = 'idle' | 'saving' | 'saved' | 'error'

type Category = 'all' | KnowledgeCategory

interface CategoryConfig {
  id: Category
  label: string
  icon: React.ElementType
  color: string
  bg: string
}

const CATEGORIES: CategoryConfig[] = [
  { id: 'all', label: 'Tudo', icon: Brain, color: 'text-bamboo-700', bg: 'bg-bamboo-50' },
  { id: 'business', label: 'Negócio', icon: Building2, color: 'text-emerald-700', bg: 'bg-emerald-50' },
  { id: 'services', label: 'Serviços', icon: Target, color: 'text-blue-700', bg: 'bg-blue-50' },
  { id: 'faq', label: 'FAQs', icon: MessageSquare, color: 'text-violet-700', bg: 'bg-violet-50' },
  { id: 'insights', label: 'Insights', icon: Lightbulb, color: 'text-amber-700', bg: 'bg-amber-50' },
  { id: 'prompts', label: 'Prompts', icon: BookOpen, color: 'text-rose-700', bg: 'bg-rose-50' },
]

// Lazy load icons helper
const IconWrapper = memo(({ icon: Icon, className }: { icon: React.ElementType; className?: string }) => (
  <Icon className={className} />
))
IconWrapper.displayName = 'IconWrapper'

// ── Generic Form Field Component ──────────────
function Field({ label, hint, children }: { label: string; hint?: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1.5 flex-1 w-full">
      <label className="block text-xs font-semibold text-bamboo-700">{label}</label>
      {children}
      {hint && <p className="text-[11px] text-bamboo-400">{hint}</p>}
    </div>
  )
}

// ── Section Component ──────────────────────────
function Section({ icon: Icon, title, children }: { icon: React.ElementType; title: string; children: React.ReactNode }) {
  return (
    <div className="card-md p-6 bg-white border border-bamboo-100 shadow-sm rounded-2xl w-full">
      <div className="flex items-center gap-2.5 mb-5 pb-4 border-b border-bamboo-100">
        <div className="w-8 h-8 rounded-xl bg-bamboo-50 flex items-center justify-center">
          <Icon className="w-4 h-4 text-bamboo-600" />
        </div>
        <h2 className="font-bold text-bamboo-900 text-sm">{title}</h2>
      </div>
      {children}
    </div>
  )
}

// ── Inline edit component ──────────────────
const ItemCard = memo(({ item, onDelete, onUpdate }: {
  item: KnowledgeItem
  onDelete: (id: string) => void
  onUpdate: (id: string, key: string, data: string) => void
}) => {
  const [editing, setEditing] = useState(false)
  const [editKey, setEditKey] = useState(item.key)
  const [editData, setEditData] = useState(
    typeof item.data === 'string' ? item.data : item.data?.content || JSON.stringify(item.data, null, 2)
  )
  const [saving, setSaving] = useState(false)
  const [expanded, setExpanded] = useState(false)

  const cat = useMemo(() =>
    CATEGORIES.find(c => c.id === item.category) || CATEGORIES[0],
    [item.category]
  )

  const content = useMemo(() =>
    typeof item.data === 'string'
      ? item.data
      : item.data?.content || JSON.stringify(item.data),
    [item.data]
  )

  async function save() {
    setSaving(true)
    await onUpdate(item.id, editKey, editData)
    setSaving(false)
    setEditing(false)
  }

  // Helper to render structured data cleanly
  const renderContent = () => {
    if (typeof item.data !== 'object' || item.data === null) return content;

    // If it's a simple content object, just show the content
    if (item.data.content && Object.keys(item.data).length === 1) return item.data.content;

    // Otherwise, render a clean list of keys
    return (
      <div className="space-y-1 mt-1">
        {Object.entries(item.data).map(([k, v]) => (
          <div key={k} className="flex gap-2 text-[10px]">
            <span className="font-bold text-bamboo-400 min-w-[60px] uppercase">{k}:</span>
            <span className="text-bamboo-600 truncate">
              {typeof v === 'object' ? JSON.stringify(v) : String(v)}
            </span>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-bamboo-100 shadow-card hover:shadow-card-md transition-all group">
      {!editing ? (
        <div className="p-4">
          {/* Card header */}
          <div className="flex items-start justify-between gap-2 mb-2">
            <div className="flex items-center gap-2 min-w-0">
              <span className={`text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full ${cat.bg} ${cat.color} flex-shrink-0`}>
                {cat.label}
              </span>
              {item.source === 'auto' && (
                <span className="text-[9px] px-1.5 py-0.5 rounded-full bg-bamboo-100 text-bamboo-600 flex items-center gap-0.5">
                  <Sparkles className="w-2 h-2" /> Auto
                </span>
              )}
            </div>
            <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0">
              <button onClick={() => setEditing(true)}
                className="w-6 h-6 rounded-lg hover:bg-bamboo-50 flex items-center justify-center text-bamboo-500 hover:text-bamboo-700">
                <Edit2 className="w-3 h-3" />
              </button>
              <button onClick={() => onDelete(item.id)}
                className="w-6 h-6 rounded-lg hover:bg-red-50 flex items-center justify-center text-gray-400 hover:text-red-500">
                <Trash2 className="w-3 h-3" />
              </button>
            </div>
          </div>

          {/* Content */}
          <p className="font-semibold text-bamboo-900 text-sm mb-1">{item.key}</p>
          <div className={`text-xs text-bamboo-500 leading-relaxed ${expanded ? '' : 'line-clamp-3'}`}>
            {renderContent()}
          </div>
          {(content.length > 100 || (typeof item.data === 'object' && Object.keys(item.data).length > 2)) && (
            <button onClick={() => setExpanded(e => !e)}
              className="mt-1.5 text-[10px] text-bamboo-500 hover:text-bamboo-700 flex items-center gap-0.5">
              {expanded ? <><ChevronUp className="w-3 h-3" />Menos</> : <><ChevronDown className="w-3 h-3" />Ver mais</>}
            </button>
          )}
        </div>
      ) : (
        <div className="p-4 space-y-2">
          <input value={editKey} onChange={e => setEditKey(e.target.value)}
            className="input-field text-sm font-semibold" placeholder="Título / chave" />

          <div className="relative group/text">
            <textarea value={editData} onChange={e => setEditData(e.target.value)}
              className="input-field text-xs resize-none h-32 pr-10 font-mono" placeholder="Conteúdo (Texto ou JSON)" />
            <button
              onClick={async () => {
                setSaving(true);
                try {
                  const res = await fetch('/api/knowledge/structure', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: editData, category: item.category })
                  }).then(r => r.json());
                  if (res.structured_data) {
                    setEditData(JSON.stringify(res.structured_data, null, 2));
                  }
                } catch (e) { console.error(e) }
                setSaving(false);
              }}
              disabled={saving}
              className="absolute right-2 top-2 p-2 bg-bamboo-100 text-bamboo-600 rounded-lg hover:bg-bamboo-600 hover:text-white transition-all shadow-sm flex items-center gap-1.5 text-[10px] font-bold"
              title="Transformar texto em código estruturado">
              <Sparkles className="w-3 h-3" /> Mágica IA
            </button>
          </div>

          <div className="flex gap-2 justify-end">
            <button onClick={() => setEditing(false)} className="btn-ghost text-xs flex items-center gap-1">
              <X className="w-3 h-3" /> Cancelar
            </button>
            <button onClick={save} disabled={saving} className="btn-primary text-xs flex items-center gap-1.5">
              {saving ? <Loader2 className="w-3 h-3 animate-spin" /> : <Check className="w-3 h-3" />}
              Salvar
            </button>
          </div>
        </div>
      )}
    </div>
  )
})
ItemCard.displayName = 'ItemCard'

// ── Add Item Form ──────────────────────────
const AddItemForm = memo(({ onAdd, onCancel }: {
  onAdd: (category: string, key: string, data: string) => Promise<void>
  onCancel: () => void
}) => {
  const [category, setCategory] = useState('services')
  const [key, setKey] = useState('')
  const [data, setData] = useState('')
  const [saving, setSaving] = useState(false)

  async function submit() {
    if (!key.trim() || !data.trim()) return
    setSaving(true)
    await onAdd(category, key, data)
    setSaving(false)
  }

  return (
    <div className="bg-bamboo-50 rounded-xl border-2 border-bamboo-300 border-dashed p-5 space-y-3">
      <h4 className="text-sm font-bold text-bamboo-800 flex items-center gap-2">
        <Plus className="w-4 h-4" /> Novo item de conhecimento
      </h4>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-[11px] font-semibold text-bamboo-700 mb-1">Categoria</label>
          <select value={category} onChange={e => setCategory(e.target.value)} className="input-field text-sm">
            <option value="business">🏢 Negócio</option>
            <option value="services">🎯 Serviços</option>
            <option value="faq">💬 FAQ</option>
            <option value="insights">💡 Insight</option>
            <option value="prompts">📖 Prompt</option>
          </select>
        </div>
        <div>
          <label className="block text-[11px] font-semibold text-bamboo-700 mb-1">Título / Chave</label>
          <input value={key} onChange={e => setKey(e.target.value)}
            className="input-field text-sm" placeholder="Ex: Preço Escova Progressiva" />
        </div>
      </div>

      <div className="relative group/text">
        <label className="block text-[11px] font-semibold text-bamboo-700 mb-1">Conteúdo</label>
        <textarea value={data} onChange={e => setData(e.target.value)}
          className="input-field text-sm resize-none h-24 pr-10"
          placeholder="Escreva em português normal ou cole um JSON..." />
        <button
          onClick={async () => {
            setSaving(true);
            try {
              const res = await fetch('/api/knowledge/structure', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: data, category: category })
              }).then(r => r.json());
              if (res.structured_data) {
                setData(JSON.stringify(res.structured_data, null, 2));
              }
            } catch (e) { console.error(e) }
            setSaving(false);
          }}
          disabled={saving || !data.trim()}
          className="absolute right-2 top-8 p-2 bg-bamboo-100 text-bamboo-600 rounded-lg hover:bg-bamboo-600 hover:text-white transition-all shadow-sm flex items-center gap-1.5 text-[10px] font-bold"
          title="Transformar texto em código estruturado">
          <Sparkles className="w-3 h-3" /> Mágica IA
        </button>
      </div>

      <div className="flex gap-2 justify-end">
        <button onClick={onCancel} className="btn-ghost text-sm">Cancelar</button>
        <button onClick={submit} disabled={saving || !key.trim() || !data.trim()}
          className="btn-primary text-sm flex items-center gap-2">
          {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
          Adicionar ao Brain
        </button>
      </div>
    </div>
  )
})
AddItemForm.displayName = 'AddItemForm'

// ── Business Section ───────────────────────
const BusinessSection = memo(({ items, onAdd }: {
  items: KnowledgeItem[]
  onAdd: (category: string, key: string, data: string) => Promise<void>
}) => {
  const [bizName, setBizName] = useState('')
  const [bizHours, setBizHours] = useState('')
  const [bizAddress, setBizAddress] = useState('')
  const [syncing, setSyncing] = useState(false)
  const [synced, setSynced] = useState(false)

  // Pre-fill from existing brain data
  useEffect(() => {
    const bizItem = items.find(i => i.category === 'business' && i.key === 'Informações do Negócio')
    if (bizItem && typeof bizItem.data === 'object') {
      const d = bizItem.data as unknown as Record<string, string>
      setBizName(d.name || '')
      setBizHours(d.hours || '')
      setBizAddress(d.address || '')
    }
  }, [items])

  async function syncBusiness() {
    setSyncing(true)
    try {
      await fetch('/api/knowledge/sync-business', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          business: { name: bizName, hours: bizHours, address: bizAddress },
        }),
      })
      setSynced(true)
      setTimeout(() => setSynced(false), 2000)
    } catch { }
    setSyncing(false)
  }

  return (
    <div className="card-md p-5 mb-6">
      <div className="flex items-center gap-2 mb-4 pb-3 border-b border-bamboo-100">
        <div className="w-6 h-6 rounded-lg bg-emerald-100 flex items-center justify-center">
          <Building2 className="w-3.5 h-3.5 text-emerald-600" />
        </div>
        <h3 className="font-bold text-bamboo-900 text-sm">Dados do Negócio</h3>
        <p className="text-[11px] text-bamboo-400 ml-auto">A Luna usa essas informações em todas as respostas</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
        <div>
          <label className="block text-[11px] font-semibold text-bamboo-700 mb-1">Nome do Estabelecimento</label>
          <input value={bizName} onChange={e => setBizName(e.target.value)}
            className="input-field text-sm" placeholder="Haven Escovaria & Esmalteria" />
        </div>
        <div>
          <label className="block text-[11px] font-semibold text-bamboo-700 mb-1">Horário de Funcionamento</label>
          <input value={bizHours} onChange={e => setBizHours(e.target.value)}
            className="input-field text-sm" placeholder="Seg–Sáb, 8h às 20h" />
        </div>
        <div>
          <label className="block text-[11px] font-semibold text-bamboo-700 mb-1">Endereço</label>
          <input value={bizAddress} onChange={e => setBizAddress(e.target.value)}
            className="input-field text-sm" placeholder="Rua, número, bairro, cidade" />
        </div>
      </div>

      <button onClick={syncBusiness} disabled={syncing}
        className="btn-primary text-sm flex items-center gap-2">
        {syncing ? <Loader2 className="w-4 h-4 animate-spin" /> :
          synced ? <Check className="w-4 h-4" /> : <Database className="w-4 h-4" />}
        {synced ? 'Sincronizado!' : 'Salvar no Brain'}
      </button>
    </div>
  )
})
BusinessSection.displayName = 'BusinessSection'

// ── Chat Simulator ─────────────────────────
interface SimulatorMessage {
  id: string
  role: 'user' | 'luna'
  content: string
  meta?: { intent: string; model: string; time_ms: number; confidence: number }
}

const QUICK_TESTS = [
  "Oi! Quanto custa a escova lisa?",
  "Tem horário essa semana com a Ju?",
  "Qual a diferença entre gel e acrílico?",
  "Vocês fazem progressiva?",
  "Tem desconto para primeira vez?",
  "Como funciona o pagamento?",
  "Onde ficam vocês?"
]

const ChatSimulator = memo(() => {
  const [messages, setMessages] = useState<SimulatorMessage[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState<string>('observe')
  const bottomRef = useRef<HTMLDivElement>(null)

  // Fetch current Luna mode
  useEffect(() => {
    fetch('/api/webhooks/mode').then(r => r.json()).then(d => setMode(d.mode)).catch(() => { })
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim() || loading) return
    const userMsg: SimulatorMessage = { id: Date.now().toString(), role: 'user', content: text }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)
    try {
      const res = await fetch('/api/brain/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, name: 'Teste Interno', phone: '5549900000001' })
      }).then(r => r.json())
      const lunaMsg: SimulatorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'luna',
        content: res.ok ? res.response : `❌ Erro: ${res.error}`,
        meta: res.ok ? { intent: res.intent, model: res.model, time_ms: res.processing_ms, confidence: res.intent_confidence } : undefined
      }
      setMessages(prev => [...prev, lunaMsg])
    } catch (e) {
      setMessages(prev => [...prev, { id: Date.now().toString(), role: 'luna', content: '❌ Erro ao conectar com o backend' }])
    }
    setLoading(false)
  }, [loading])

  return (
    <div className="flex flex-col gap-4">
      {/* Mode badge */}
      <div className="flex items-center gap-3">
        <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold border ${mode === 'observe' ? 'bg-amber-50 text-amber-700 border-amber-200' : 'bg-green-50 text-green-700 border-green-200'
          }`}>
          <span className={`w-1.5 h-1.5 rounded-full animate-pulse ${mode === 'observe' ? 'bg-amber-400' : 'bg-green-400'}`} />
          {mode === 'observe' ? '🔇 Modo Observação — Luna não responde ao WhatsApp' : '🟢 Modo Ativo — Luna está respondendo'}
        </div>
        <button onClick={() => {
          const newMode = mode === 'observe' ? 'active' : 'observe'
          fetch('/api/webhooks/mode', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ mode: newMode }) })
            .then(r => r.json()).then(d => setMode(d.mode))
        }} className="ml-auto text-xs text-bamboo-500 hover:text-bamboo-800 underline">
          Alternar para {mode === 'observe' ? 'Ativo' : 'Observação'}
        </button>
      </div>

      {/* Quick tests */}
      <div>
        <p className="text-[11px] text-bamboo-400 font-semibold mb-2">TESTES RÁPIDOS</p>
        <div className="flex flex-wrap gap-2">
          {QUICK_TESTS.map(t => (
            <button key={t} onClick={() => sendMessage(t)}
              className="px-3 py-1.5 text-xs bg-white border border-bamboo-200 rounded-full text-bamboo-600 hover:border-bamboo-400 hover:text-bamboo-900 transition-all">
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Chat window */}
      <div className="bg-white border border-bamboo-100 rounded-2xl shadow-card overflow-hidden flex flex-col" style={{ height: 480 }}>
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-center gap-3">
              <div className="w-12 h-12 rounded-full bg-bamboo-100 flex items-center justify-center">
                <MessageSquare className="w-6 h-6 text-bamboo-400" />
              </div>
              <div>
                <p className="font-semibold text-bamboo-700">Simulador de Conversa</p>
                <p className="text-sm text-bamboo-400 mt-1">Digite uma mensagem para testar a Luna internamente</p>
              </div>
            </div>
          )}
          {messages.map(msg => (
            <div key={msg.id} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-bold ${msg.role === 'luna' ? 'bg-bamboo-100 text-bamboo-600' : 'bg-blue-100 text-blue-600'
                }`}>
                {msg.role === 'luna' ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
              </div>
              <div className={`max-w-[75%] space-y-1 ${msg.role === 'user' ? 'items-end' : 'items-start'} flex flex-col`}>
                <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${msg.role === 'luna'
                  ? 'bg-bamboo-50 text-bamboo-900 rounded-tl-sm'
                  : 'bg-blue-500 text-white rounded-tr-sm'
                  }`}>
                  {msg.content}
                </div>
                {msg.meta && (
                  <div className="flex flex-wrap gap-1.5 px-1">
                    <span className="px-2 py-0.5 bg-violet-50 text-violet-600 rounded-full text-[10px] font-semibold border border-violet-100">
                      🎯 {msg.meta.intent} ({Math.round(msg.meta.confidence * 100)}%)
                    </span>
                    <span className="px-2 py-0.5 bg-blue-50 text-blue-600 rounded-full text-[10px] font-semibold border border-blue-100">
                      🤖 {msg.meta.model.split('/').pop()}
                    </span>
                    <span className="px-2 py-0.5 bg-gray-50 text-gray-500 rounded-full text-[10px] font-semibold border border-gray-100">
                      ⏱ {msg.meta.time_ms}ms
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex gap-3">
              <div className="w-7 h-7 rounded-full bg-bamboo-100 flex items-center justify-center">
                <Bot className="w-4 h-4 text-bamboo-600" />
              </div>
              <div className="px-4 py-3 bg-bamboo-50 rounded-2xl rounded-tl-sm">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-bamboo-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 bg-bamboo-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 bg-bamboo-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="border-t border-bamboo-100 p-3 flex gap-2">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !e.shiftKey && sendMessage(input)}
            placeholder="Digite uma mensagem como cliente..."
            className="flex-1 px-4 py-2.5 bg-bamboo-50 border border-bamboo-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-bamboo-400"
          />
          <button onClick={() => sendMessage(input)} disabled={loading || !input.trim()}
            className="px-4 py-2.5 bg-bamboo-600 text-white rounded-xl hover:bg-bamboo-700 disabled:opacity-40 transition-all">
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          </button>
          {messages.length > 0 && (
            <button onClick={() => setMessages([])} className="p-2.5 text-bamboo-400 hover:text-bamboo-600 rounded-xl hover:bg-bamboo-50 transition-all" title="Limpar">
              <RefreshCw className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  )
})
ChatSimulator.displayName = 'ChatSimulator'

// ── Main Page ──────────────────────────────
export default function BrainPage() {
  const [activeTab, setActiveTab] = useState<'simulator' | 'knowledge' | 'persona'>('simulator')
  const [items, setItems] = useState<KnowledgeItem[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState<Category>('all')
  const [showForm, setShowForm] = useState(false)

  // New States for Persona settings
  const [botName, setBotName] = useState('Luna')
  const [greeting, setGreeting] = useState('')
  const [fallback, setFallback] = useState('')
  const [bizName, setBizName] = useState('')
  const [bizHours, setBizHours] = useState('')
  const [saveStatus, setSaveStatus] = useState<SaveStatus>('idle')
  const [savingSettings, setSavingSettings] = useState(false)

  const fetchItems = useCallback(async () => {
    try {
      const d = await fetch('/api/knowledge').then(r => r.json())
      setItems(Array.isArray(d) ? d : [])
    } catch { setItems([]) }
    setLoading(false)
  }, [])

  useEffect(() => {
    fetchItems()

    // Fetch generic settings on mount
    fetch('/api/settings')
      .then(r => r.json())
      .then(d => {
        setBotName(d.bot?.name || 'Luna')
        setGreeting(d.bot?.greeting || '')
        setFallback(d.bot?.fallback || '')
        setBizName(d.business?.name || '')
        setBizHours(d.business?.hours || '')
      })
      .catch(e => console.error("Falha ao carregar settings da Luna", e))
  }, [fetchItems])

  // Save Persona function
  async function savePersona() {
    setSavingSettings(true)
    setSaveStatus('idle')
    try {
      const r = await fetch('/api/settings/', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bot: { name: botName, greeting, fallback },
          business: { name: bizName, hours: bizHours },
        }),
      })
      setSaveStatus(r.ok ? 'saved' : 'error')
    } catch {
      setSaveStatus('error')
    } finally {
      setSavingSettings(false)
      setTimeout(() => setSaveStatus('idle'), 3000)
    }
  }

  async function addItem(cat: string, key: string, data: string) {
    await fetch('/api/knowledge/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category: cat, key, data: { content: data }, source: 'manual' }),
    })
    setShowForm(false)
    fetchItems()
  }

  async function updateItem(id: string, key: string, data: string) {
    await fetch(`/api/knowledge/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category: 'services', key, data: { content: data } }),
    })
    fetchItems()
  }

  async function deleteItem(id: string) {
    if (!confirm('Remover este item do Brain?')) return
    await fetch(`/api/knowledge/${id}`, { method: 'DELETE' })
    setItems(prev => prev.filter(i => i.id !== id))
  }

  const filtered = items.filter(item => {
    const matchCat = category === 'all' || item.category === category
    const matchSearch = !search || item.key.toLowerCase().includes(search.toLowerCase()) ||
      JSON.stringify(item.data).toLowerCase().includes(search.toLowerCase())
    return matchCat && matchSearch
  })

  const counts = {
    business: items.filter(i => i.category === 'business').length,
    services: items.filter(i => i.category === 'services').length,
    faq: items.filter(i => i.category === 'faq').length,
    insights: items.filter(i => i.category === 'insights').length,
    prompts: items.filter(i => i.category === 'prompts').length,
    total: items.length,
  }

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-bamboo-50/30">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-start justify-between">
          <div>
            <p className="section-label mb-1">Inteligência Contínua</p>
            <h1 className="text-2xl font-extrabold text-bamboo-900 flex items-center gap-3">
              <Brain className="w-7 h-7 text-bamboo-600" /> Brain da Luna
            </h1>
            <p className="text-sm text-bamboo-500 mt-0.5">
              Simule conversas e edite o conhecimento da Luna
            </p>
          </div>
          {activeTab === 'knowledge' && (
            <button onClick={() => setShowForm(s => !s)}
              className="btn-primary flex items-center gap-2 text-sm">
              <Plus className="w-4 h-4" /> Adicionar Conhecimento
            </button>
          )}
        </div>

        {/* Tabs */}
        <div className="flex gap-1 bg-bamboo-100 rounded-xl p-1 w-fit">
          <button onClick={() => setActiveTab('simulator')}
            className={`flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-semibold transition-all ${activeTab === 'simulator' ? 'bg-white shadow-card text-bamboo-900' : 'text-bamboo-500 hover:text-bamboo-700'
              }`}>
            <MessageSquare className="w-4 h-4" /> 💬 Simulador
          </button>
          <button onClick={() => setActiveTab('knowledge')}
            className={`flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-semibold transition-all ${activeTab === 'knowledge' ? 'bg-white shadow-card text-bamboo-900' : 'text-bamboo-500 hover:text-bamboo-700'
              }`}>
            <Brain className="w-4 h-4" /> 📚 Knowledge Base
          </button>
          <button onClick={() => setActiveTab('persona')}
            className={`flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-semibold transition-all ${activeTab === 'persona' ? 'bg-white shadow-card text-bamboo-900' : 'text-bamboo-500 hover:text-bamboo-700'
              }`}>
            <User className="w-4 h-4" /> 🎭 Persona & Negócio
          </button>
        </div>

        {/* TAB: Simulator */}
        {activeTab === 'simulator' && <ChatSimulator />}

        {/* TAB: Knowledge Base */}
        {activeTab === 'knowledge' && (
          <>
            {/* Add form */}
            {showForm && <AddItemForm onAdd={addItem} onCancel={() => setShowForm(false)} />}

            {/* Stats */}
            <div className="grid grid-cols-3 lg:grid-cols-6 gap-3">
              {[
                { label: 'Total', value: counts.total, color: 'text-bamboo-700', bg: 'bg-bamboo-50', border: 'border-bamboo-200' },
                { label: 'Negócio', value: counts.business, color: 'text-emerald-700', bg: 'bg-emerald-50', border: 'border-emerald-200' },
                { label: 'Serviços', value: counts.services, color: 'text-blue-700', bg: 'bg-blue-50', border: 'border-blue-200' },
                { label: 'FAQs', value: counts.faq, color: 'text-violet-700', bg: 'bg-violet-50', border: 'border-violet-200' },
                { label: 'Insights', value: counts.insights, color: 'text-amber-700', bg: 'bg-amber-50', border: 'border-amber-200' },
                { label: 'Prompts', value: counts.prompts, color: 'text-rose-700', bg: 'bg-rose-50', border: 'border-rose-200' },
              ].map(s => (
                <div key={s.label} className={`${s.bg} border ${s.border} rounded-xl p-3 text-center shadow-card`}>
                  <p className={`text-2xl font-extrabold ${s.color}`}>{s.value}</p>
                  <p className="text-[10px] text-bamboo-500 font-medium mt-0.5">{s.label}</p>
                </div>
              ))}
            </div>

            {/* Filters + Search */}
            <div className="flex flex-col sm:flex-row gap-3 items-start sm:items-center">
              <div className="flex gap-1.5 flex-wrap">
                {CATEGORIES.map(cat => (
                  <button key={cat.id} onClick={() => setCategory(cat.id)}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all border
                  ${category === cat.id
                        ? `${cat.bg} ${cat.color} border-current shadow-card`
                        : 'bg-white text-bamboo-600 border-bamboo-200 hover:border-bamboo-400'
                      }`}>
                    <cat.icon className="w-3 h-3" />
                    {cat.label}
                    {cat.id !== 'all' && <span className="ml-0.5 opacity-60">{counts[cat.id as keyof typeof counts]}</span>}
                  </button>
                ))}
              </div>
              <div className="relative flex-1 min-w-[200px]">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-bamboo-400" />
                <input type="text" value={search} onChange={e => setSearch(e.target.value)}
                  placeholder="Buscar no Brain..."
                  className="input-field pl-9 text-sm w-full" />
              </div>
            </div>

            {/* Content grid */}
            {loading ? (
              <div className="py-16 text-center">
                <Loader2 className="w-8 h-8 text-bamboo-500 animate-spin mx-auto" />
              </div>
            ) : filtered.length === 0 ? (
              <div className="py-16 text-center bg-white rounded-2xl border-2 border-dashed border-bamboo-200 shadow-card">
                <Brain className="w-12 h-12 text-bamboo-200 mx-auto mb-3" />
                <p className="font-bold text-bamboo-600">
                  {search ? `Nenhum resultado para "${search}"` : 'Brain vazio nesta categoria'}
                </p>
                <p className="text-sm text-bamboo-400 mt-1">Adicione conhecimento para a Luna aprender</p>
                <button onClick={() => setShowForm(true)}
                  className="btn-primary mt-4 mx-auto flex items-center gap-2 text-sm">
                  <Plus className="w-4 h-4" /> Adicionar primeiro item
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filtered.map(item => (
                  <ItemCard key={item.id} item={item}
                    onDelete={deleteItem}
                    onUpdate={updateItem} />
                ))}
              </div>
            )}

            {/* Continuous learning note */}
            <div className="flex items-start gap-3 p-4 bg-bamboo-50 border border-bamboo-200 rounded-xl">
              <Sparkles className="w-4 h-4 text-bamboo-500 flex-shrink-0 mt-0.5" />
              <p className="text-xs text-bamboo-600 leading-relaxed">
                <strong>Aprendizado Contínuo:</strong> Cada conversa que a Luna tem pode gerar novos Insights automaticamente.
                Adicione informações manualmente aqui ou conecte via Supabase — a Luna consulta este Brain em tempo real antes de cada resposta.
              </p>
            </div>
          </>
        )}

        {/* TAB: Persona & Negócio */}
        {activeTab === 'persona' && (
          <div className="space-y-6 max-w-4xl mx-auto py-2">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h3 className="text-xl font-bold text-bamboo-900">Personalidade e Informações Base</h3>
                <p className="text-sm text-bamboo-500">Ajuste o tom e os dados estruturais do assistente.</p>
              </div>
              <button onClick={savePersona} disabled={savingSettings}
                className={`btn-primary flex items-center justify-center gap-2 text-sm px-6
                  ${saveStatus === 'saved' ? 'bg-bamboo-600' : ''}
                  ${saveStatus === 'error' ? 'bg-red-500 hover:bg-red-600' : ''}
                `}>
                {savingSettings ? <Loader2 className="w-4 h-4 animate-spin" /> :
                  saveStatus === 'saved' ? <CheckCircle className="w-4 h-4" /> :
                    saveStatus === 'error' ? <AlertCircle className="w-4 h-4" /> :
                      <Save className="w-4 h-4" />}
                {saveStatus === 'saved' ? 'Salvo!' : saveStatus === 'error' ? 'Erro' : 'Salvar Persona'}
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* ── Personalidade da Luna ─────────────── */}
              <Section icon={Bot} title="Identidade do Bot">
                <div className="space-y-5">
                  <Field label="Nome do Agente" hint="O nome pelo qual ela se apresentará nas conversas.">
                    <input className="input-field" value={botName} onChange={e => setBotName(e.target.value)} />
                  </Field>
                  <Field label="Saudação Inicial" hint="Primeira mensagem enviada quando iniciam contato. Mantenha curta.">
                    <textarea className="input-field resize-none h-24" value={greeting} onChange={e => setGreeting(e.target.value)} />
                  </Field>
                  <Field label="Fallback" hint="Frase de escape usada se a IA não conseguir lidar com o contexto ou der falha.">
                    <input className="input-field" value={fallback} onChange={e => setFallback(e.target.value)} />
                  </Field>
                </div>
              </Section>

              {/* ── Dados do Negócio ──────────────────── */}
              <Section icon={Building2} title="Metadados do Negócio">
                <div className="space-y-5 flex flex-col h-full">
                  <Field label="Nome do Estabelecimento" hint="Nome fantasia usado nas assinaturas e confirmações.">
                    <input className="input-field" value={bizName} onChange={e => setBizName(e.target.value)} />
                  </Field>
                  <Field label="Horário de Funcionamento" hint="Em qual intervalo a IA considerará aberto/fechado.">
                    <input className="input-field" value={bizHours} onChange={e => setBizHours(e.target.value)} placeholder="Ex: Segunda a Sábado, 8h às 20h" />
                  </Field>

                  <div className="mt-auto pt-6">
                    <div className="bg-bamboo-50 rounded-xl p-4 border border-bamboo-200">
                      <div className="flex items-start gap-3">
                        <Database className="w-5 h-5 text-bamboo-600 flex-shrink-0 mt-0.5" />
                        <div>
                          <p className="text-sm font-semibold text-bamboo-900">Truth in Data</p>
                          <p className="text-xs text-bamboo-500 mt-1 leading-relaxed">
                            A base de conhecimento (Knowledge Base) é preenchida na outra aba. Se a loja mudar de endereço ou o preço de um serviço mudar, centralizamos os dados ali, evitando edição de prompts soltos e mantendo a fonte de verdade limpa no banco.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Section>
            </div>
          </div>
        )}

      </div>
    </div>
  )
}
