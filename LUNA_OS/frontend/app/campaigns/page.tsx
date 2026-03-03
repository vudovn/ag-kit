"use client";

import { useState, useEffect } from 'react'
import { Megaphone, Plus, Loader2, Radio, CheckCircle, Clock, X, Save, Users, Type, CalendarRange, Target, Zap } from 'lucide-react'

interface Campaign {
  id: string
  name: string
  type: string
  status: string
  created_at: string
  target_segment?: string
  start_date?: string
  end_date?: string
  objective?: string
}

const STATUS_STYLE: Record<string, { label: string; color: string; icon: any }> = {
  active: { label: 'Ativa', color: 'text-bamboo-700 bg-bamboo-50 border-bamboo-300', icon: Radio },
  completed: { label: 'Concluída', color: 'text-gray-600 bg-gray-50 border-gray-200', icon: CheckCircle },
  scheduled: { label: 'Agendada', color: 'text-blue-700 bg-blue-50 border-blue-200', icon: Clock },
  draft: { label: 'Rascunho', color: 'text-amber-700 bg-amber-50 border-amber-200', icon: Clock },
}

const TYPE_LABEL: Record<string, string> = {
  reativacao: 'Reativação',
  promocao: 'Promoção',
  lembrete: 'Lembrete',
  follow_up: 'Follow-up',
  aniversario: 'Aniversário',
  informativa: 'Informativa',
}

function NewCampaignModal({ onClose, onCreated }: { onClose: () => void; onCreated: (c: Campaign) => void }) {
  const [name, setName] = useState('')
  const [type, setType] = useState('reativacao')
  const [segment, setSegment] = useState('todos')
  const [objective, setObjective] = useState('venda')
  const [objectiveDesc, setObjectiveDesc] = useState('')
  const [insights, setInsights] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  async function submit() {
    if (!name.trim()) { setError('Nome da campanha é obrigatório'); return }
    if (startDate && endDate && endDate < startDate) { setError('Data de término deve ser após a data de início'); return }
    setSaving(true)
    setError('')
    try {
      const r = await fetch('/api/campaigns/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name,
          type,
          target_segment: segment,
          status: 'draft',
          objective,
          objective_description: objectiveDesc,
          insights,
          start_date: startDate || null,
          end_date: endDate || null,
        }),
      })
      if (!r.ok) throw new Error(await r.text())
      const created = await r.json()
      onCreated(created)
      onClose()
    } catch (e: any) {
      setError(e.message || 'Erro ao criar campanha')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-card-lg w-full max-w-lg border border-bamboo-100 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-bamboo-100 sticky top-0 bg-white z-10">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-bamboo-100 flex items-center justify-center">
              <Megaphone className="w-4 h-4 text-bamboo-600" />
            </div>
            <h3 className="font-bold text-bamboo-900">Nova Campanha</h3>
          </div>
          <button onClick={onClose} className="w-7 h-7 rounded-lg hover:bg-bamboo-50 flex items-center justify-center text-bamboo-400 hover:text-bamboo-700">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body */}
        <div className="p-5 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-bamboo-700 mb-1.5">Nome da Campanha *</label>
            <input value={name} onChange={e => setName(e.target.value)}
              className="input-field" placeholder="Ex: Reativação Clientes Inativos 30d" />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-bamboo-700 mb-1.5">Tipo</label>
              <select value={type} onChange={e => setType(e.target.value)} className="input-field">
                <option value="reativacao">Reativação de clientes</option>
                <option value="promocao">Promoção / Oferta</option>
                <option value="lembrete">Lembrete de agendamento</option>
                <option value="follow_up">Follow-up pós-visita</option>
                <option value="aniversario">Aniversário de cliente</option>
                <option value="informativa">Mensagem informativa</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-bamboo-700 mb-1.5">Segmento Alvo</label>
              <select value={segment} onChange={e => setSegment(e.target.value)} className="input-field">
                <option value="todos">Todos os clientes</option>
                <option value="inativos_30">Inativos há 30+ dias</option>
                <option value="inativos_60">Inativos há 60+ dias</option>
                <option value="recorrentes">Clientes recorrentes</option>
                <option value="novos">Clientes novos (1ª visita)</option>
              </select>
            </div>
          </div>

          {/* ── Datas de Vigência ── */}
          <div>
            <label className="block text-xs font-semibold text-bamboo-700 mb-1.5 flex items-center gap-1">
              <CalendarRange className="w-3.5 h-3.5" /> Período da Campanha
            </label>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-[10px] text-bamboo-500 mb-1">Data de Início</label>
                <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)}
                  className="input-field text-sm" />
              </div>
              <div>
                <label className="block text-[10px] text-bamboo-500 mb-1">Data de Término</label>
                <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)}
                  className="input-field text-sm" />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-bamboo-700 mb-1.5">Objetivo Principal</label>
            <select value={objective} onChange={e => setObjective(e.target.value)} className="input-field">
              <option value="venda">Venda Direta (agendamento)</option>
              <option value="reativacao">Reativação (clientes sumidos)</option>
              <option value="branding">Brand Awareness (lembrar da marca)</option>
              <option value="followup">Follow-up (pós-atendimento)</option>
              <option value="oportunidade">Oportunidade durante conversa</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-bamboo-700 mb-1.5">Descrição do Objetivo</label>
            <textarea value={objectiveDesc} onChange={e => setObjectiveDesc(e.target.value)}
              className="input-field resize-none h-16 text-sm"
              placeholder="Ex: Quero agendar 20 clientes para a semana do Dia das Mães" />
          </div>

          <div>
            <label className="block text-xs font-semibold text-bamboo-700 mb-1.5">
              Insights / Contexto para IA
              <span className="text-bamboo-400 font-normal ml-1">(opcional)</span>
            </label>
            <textarea value={insights} onChange={e => setInsights(e.target.value)}
              className="input-field resize-none h-20 text-sm"
              placeholder={"Ex: Mães costumam preferir atendimento pela manhã.\nOfereça pacote cabelo+unha com 15% OFF.\nEvite falar em preço logo de cara."} />
            <p className="text-[10px] text-bamboo-400 mt-1">
              💡 Essas informações ajudam a Luna a personalizar a mensagem da campanha
            </p>
          </div>

          {error && (
            <div className="text-xs text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
              {error}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex gap-2 justify-end p-5 border-t border-bamboo-100 sticky bottom-0 bg-white">
          <button onClick={onClose} className="btn-ghost text-sm">Cancelar</button>
          <button onClick={submit} disabled={saving || !name.trim()}
            className="btn-primary text-sm flex items-center gap-2">
            {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
            {saving ? 'Criando...' : 'Criar Campanha'}
          </button>
        </div>
      </div>
    </div>
  )
}

// Campanhas de exemplo populadas com contexto real do Haven
const EXAMPLE_CAMPAIGNS: Campaign[] = [
  {
    id: 'ex-1',
    name: 'Reativação — Clientes Inativos 30d',
    type: 'reativacao',
    status: 'active',
    created_at: new Date().toISOString(),
    target_segment: 'inativos_30',
    start_date: '2026-03-01',
    end_date: '2026-03-31',
    objective: 'reativacao',
  },
  {
    id: 'ex-2',
    name: 'Promoção Dia das Mães — Pacote Cabelo + Unha',
    type: 'promocao',
    status: 'scheduled',
    created_at: new Date().toISOString(),
    target_segment: 'recorrentes',
    start_date: '2026-05-01',
    end_date: '2026-05-11',
    objective: 'venda',
  },
  {
    id: 'ex-3',
    name: 'Follow-up Pós Progressiva (48h)',
    type: 'follow_up',
    status: 'active',
    created_at: new Date().toISOString(),
    target_segment: 'todos',
    objective: 'followup',
  },
]

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    fetch('/api/campaigns')
      .then(r => r.json())
      .then(d => setCampaigns(Array.isArray(d) && d.length > 0 ? d : EXAMPLE_CAMPAIGNS))
      .catch(() => setCampaigns(EXAMPLE_CAMPAIGNS))
      .finally(() => setLoading(false))
  }, [])

  function handleCreated(c: Campaign) {
    setCampaigns(prev => [c, ...prev])
  }

  // Stats
  const active = campaigns.filter(c => c.status === 'active').length
  const scheduled = campaigns.filter(c => c.status === 'scheduled').length

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-bamboo-50/30">
      <div className="max-w-4xl mx-auto space-y-6">

        <div className="flex items-start justify-between">
          <div>
            <p className="section-label mb-1">WhatsApp</p>
            <h1 className="text-2xl font-extrabold text-bamboo-900">Campanhas</h1>
            <p className="text-sm text-bamboo-500 mt-0.5">Mensagens em massa e automações de reativação</p>
          </div>
          <button onClick={() => setShowModal(true)}
            className="btn-primary flex items-center gap-2 text-sm">
            <Plus className="w-4 h-4" /> Nova Campanha
          </button>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-3 gap-4">
          {[
            { label: 'Ativas', value: active, color: 'text-bamboo-700', bg: 'bg-bamboo-50 border-bamboo-200', icon: Zap },
            { label: 'Agendadas', value: scheduled, color: 'text-blue-700', bg: 'bg-blue-50 border-blue-200', icon: CalendarRange },
            { label: 'Total', value: campaigns.length, color: 'text-gray-700', bg: 'bg-gray-50 border-gray-200', icon: Target },
          ].map(stat => (
            <div key={stat.label} className={`flex items-center gap-3 p-4 rounded-2xl border ${stat.bg}`}>
              <stat.icon className={`w-5 h-5 ${stat.color}`} />
              <div>
                <p className={`text-xl font-black ${stat.color}`}>{stat.value}</p>
                <p className="text-[11px] text-gray-500 font-semibold">{stat.label}</p>
              </div>
            </div>
          ))}
        </div>

        {loading ? (
          <div className="py-20 text-center"><Loader2 className="w-8 h-8 text-bamboo-500 animate-spin mx-auto" /></div>
        ) : campaigns.length === 0 ? (
          <div className="py-20 text-center bg-white rounded-2xl border-2 border-dashed border-bamboo-200 shadow-card">
            <Megaphone className="w-14 h-14 text-bamboo-200 mx-auto mb-4" />
            <p className="text-bamboo-700 font-bold text-lg">Nenhuma campanha ainda</p>
            <p className="text-sm text-bamboo-400 mt-2 max-w-sm mx-auto leading-relaxed">
              Crie campanhas para reativar clientes inativos, divulgar promoções ou fazer follow-ups automáticos.
            </p>
            <button onClick={() => setShowModal(true)}
              className="btn-primary mt-5 mx-auto flex items-center gap-2 text-sm">
              <Plus className="w-4 h-4" /> Criar primeira campanha
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {campaigns.map(c => {
              const style = STATUS_STYLE[c.status] || STATUS_STYLE.draft
              const Icon = style.icon
              return (
                <div key={c.id} className="bg-white rounded-2xl border border-bamboo-100 shadow-card hover:shadow-card-md transition-all p-5 flex items-center gap-5">
                  <div className="w-11 h-11 bg-bamboo-50 rounded-xl flex items-center justify-center flex-shrink-0 border border-bamboo-100">
                    <Megaphone className="w-5 h-5 text-bamboo-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-bold text-bamboo-900">{c.name}</p>
                    <div className="flex flex-wrap items-center gap-3 mt-1">
                      <span className="flex items-center gap-1 text-xs text-bamboo-500">
                        <Type className="w-3 h-3" /> {TYPE_LABEL[c.type] || c.type}
                      </span>
                      <span className="flex items-center gap-1 text-xs text-bamboo-500">
                        <Users className="w-3 h-3" /> {c.target_segment || 'Todos'}
                      </span>
                      {(c.start_date || c.end_date) && (
                        <span className="flex items-center gap-1 text-xs text-bamboo-400 bg-bamboo-50 px-2 py-0.5 rounded-full border border-bamboo-100">
                          <CalendarRange className="w-3 h-3" />
                          {c.start_date ? new Date(c.start_date + 'T00:00:00').toLocaleDateString('pt-BR') : '?'}
                          {' → '}
                          {c.end_date ? new Date(c.end_date + 'T00:00:00').toLocaleDateString('pt-BR') : 'Sem fim'}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-xs font-bold ${style.color}`}>
                    <Icon className="w-3 h-3" /> {style.label}
                  </div>
                  <p className="text-xs text-bamboo-400 flex-shrink-0">
                    {new Date(c.created_at).toLocaleDateString('pt-BR')}
                  </p>
                </div>
              )
            })}
          </div>
        )}

      </div>

      {showModal && <NewCampaignModal onClose={() => setShowModal(false)} onCreated={handleCreated} />}
    </div>
  )
}
