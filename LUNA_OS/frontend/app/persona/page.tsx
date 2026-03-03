"use client";

import { useState } from 'react'
import {
  UserCircle2, Plus, Target, TrendingUp, ShoppingBag,
  Clock, MessageCircle, Sparkles, X, Save, Loader2, Trash2, ChevronDown, ChevronUp
} from 'lucide-react'

interface Persona {
  id: string
  name: string
  icon: string
  description: string
  tags: string[]
  triggers: string[]
  color: string
  accent: string
  badge: string
}

const DEFAULTS: Persona[] = [
  {
    id: 'recorrente',
    name: 'Fiel Semanal',
    icon: '💜',
    description: 'Frequenta toda semana. Tem profissional favorita e horário fixo. Alta previsibilidade de agenda e receita mensal garantida.',
    tags: ['Fiel', 'Alto LTV', 'Indicadora', 'Horário Fixo'],
    triggers: [
      'Confirmar horário com 2 dias de antecedência',
      'Lembrar nome da profissional preferida',
      'Oferecer pacote mensal com desconto de fidelidade',
      'Priorizar quando a agenda estiver lotada',
    ],
    color: 'bg-violet-50 border-violet-200',
    accent: 'text-violet-700',
    badge: 'bg-violet-100 text-violet-700',
  },
  {
    id: 'noiva_evento',
    name: 'Noiva / Evento Social',
    icon: '👰',
    description: 'Quer Cabelo + Maquiagem + Unhas para um evento especial. Alta expectativa, prazo rígido e orçamento geralmente flexível.',
    tags: ['Alto Ticket', 'Evento Especial', 'Pontualidade Crítica'],
    triggers: [
      'Perguntar data e horário do evento logo no início',
      'Informar o tempo total estimado (~3h para pacote completo)',
      'Lembrar que maquiagem é sempre o último serviço',
      'Oferecer pacote Noiva/Evento com desconto progressivo',
      'Confirmar agendamento com 24h de antecedência',
    ],
    color: 'bg-rose-50 border-rose-200',
    accent: 'text-rose-700',
    badge: 'bg-rose-100 text-rose-700',
  },
  {
    id: 'preco',
    name: 'Sensível a Preço',
    icon: '💚',
    description: 'Pergunta o valor antes de qualquer coisa. Compara preços, responde bem a pacotes combinados e promoções com urgência.',
    tags: ['Pacotes', 'Comparadora', 'Custo-Benefício'],
    triggers: [
      'Apresentar pacotes combinados (mais valor pelo mesmo custo)',
      'Destacar que economiza tempo combinando serviços',
      'Mencionar qualidade dos produtos utilizados (Cadiveu, Keratina)',
      'Oferecer cupom para segunda visita',
      'Nunca competir em preço — agregar valor ao serviço',
    ],
    color: 'bg-bamboo-50 border-bamboo-200',
    accent: 'text-bamboo-700',
    badge: 'bg-bamboo-100 text-bamboo-700',
  },
  {
    id: 'conectada',
    name: 'Conectada (Redes Sociais)',
    icon: '📱',
    description: 'Veio pelo Instagram ou story de uma amiga. Quer resultado fotogênico. Costuma postar o resultado e virar embaixadora do salão.',
    tags: ['Influência', 'Redes Sociais', 'Resultado Visual'],
    triggers: [
      'Perguntar o look desejado (foto de referência)',
      'Mencionar durabilidade do efeito e produtos premium',
      'Incentivar a marcar @havenescovaria nos stories',
      'Oferecer desconto na próxima visita por indicação',
    ],
    color: 'bg-pink-50 border-pink-200',
    accent: 'text-pink-700',
    badge: 'bg-pink-100 text-pink-700',
  },
  {
    id: 'pressa',
    name: 'Cliente com Pressa',
    icon: '⚡',
    description: 'Pouco tempo disponível. Quer maximizar sem estender o horário. Ideal para oferecer simultaneidade de serviços.',
    tags: ['Cronograma Rígido', 'Simultaneidade', 'Eficiência'],
    triggers: [
      'Perguntar quanto tempo disponível logo no primeiro contato',
      'Propor fazer unhas durante a pausa da progressiva (economiza ~1h)',
      'Confirmar todos os serviços antes de fechar o horário',
      'Ser conservador com estimativas de tempo — nunca prometer menos',
    ],
    color: 'bg-amber-50 border-amber-200',
    accent: 'text-amber-700',
    badge: 'bg-amber-100 text-amber-700',
  },
]

function NewPersonaModal({ onClose, onCreated }: {
  onClose: () => void
  onCreated: (p: Persona) => void
}) {
  const [name, setName] = useState('')
  const [icon, setIcon] = useState('🎯')
  const [description, setDescription] = useState('')
  const [tags, setTags] = useState('')
  const [triggers, setTriggers] = useState('')
  const [saving, setSaving] = useState(false)

  function submit() {
    if (!name.trim()) return
    setSaving(true)
    const persona: Persona = {
      id: name.toLowerCase().replace(/\s+/g, '-') + '-' + Date.now(),
      name, icon, description,
      tags: tags.split(',').map(t => t.trim()).filter(Boolean),
      triggers: triggers.split('\n').map(t => t.trim()).filter(Boolean),
      color: 'bg-bamboo-50 border-bamboo-200',
      accent: 'text-bamboo-700',
      badge: 'bg-bamboo-100 text-bamboo-700',
    }
    onCreated(persona)
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-card-lg w-full max-w-md border border-bamboo-100 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-5 border-b border-bamboo-100">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-bamboo-100 flex items-center justify-center">
              <UserCircle2 className="w-4 h-4 text-bamboo-600" />
            </div>
            <h3 className="font-bold text-bamboo-900">Nova Persona</h3>
          </div>
          <button onClick={onClose} className="w-7 h-7 rounded-lg hover:bg-bamboo-50 flex items-center justify-center text-bamboo-400">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5 space-y-4">
          <div className="flex gap-3">
            <div className="w-20">
              <label className="block text-xs font-semibold text-bamboo-700 mb-1">Emoji</label>
              <input value={icon} onChange={e => setIcon(e.target.value)}
                className="input-field text-center text-xl" maxLength={2} />
            </div>
            <div className="flex-1">
              <label className="block text-xs font-semibold text-bamboo-700 mb-1">Nome *</label>
              <input value={name} onChange={e => setName(e.target.value)}
                className="input-field" placeholder="Ex: Cliente Ansioso" />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-bamboo-700 mb-1">Descrição</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)}
              className="input-field resize-none h-16 text-sm" placeholder="Como reconhecer este perfil..." />
          </div>

          <div>
            <label className="block text-xs font-semibold text-bamboo-700 mb-1">Tags (separadas por vírgula)</label>
            <input value={tags} onChange={e => setTags(e.target.value)}
              className="input-field text-sm" placeholder="Urgente, Exigente, Frequente" />
          </div>

          <div>
            <label className="block text-xs font-semibold text-bamboo-700 mb-1">Como a Luna deve agir (uma por linha)</label>
            <textarea value={triggers} onChange={e => setTriggers(e.target.value)}
              className="input-field resize-none h-20 text-sm"
              placeholder={"Responder com rapidez\nOferecer horários alternativos\nEvitar pressão por vendas"} />
          </div>
        </div>

        <div className="flex gap-2 justify-end p-5 border-t border-bamboo-100">
          <button onClick={onClose} className="btn-ghost text-sm">Cancelar</button>
          <button onClick={submit} disabled={!name.trim() || saving}
            className="btn-primary text-sm flex items-center gap-2">
            {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
            Criar Persona
          </button>
        </div>
      </div>
    </div>
  )
}

export default function PersonaPage() {
  const [personas, setPersonas] = useState<Persona[]>(DEFAULTS)
  const [selected, setSelected] = useState<string | null>(null)
  const [showModal, setShowModal] = useState(false)

  function handleCreated(p: Persona) {
    setPersonas(prev => [...prev, p])
  }

  function deletePersona(id: string) {
    if (DEFAULTS.some(d => d.id === id)) return // protect defaults
    setPersonas(prev => prev.filter(p => p.id !== id))
  }

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-bamboo-50/30">
      <div className="max-w-5xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-start justify-between">
          <div>
            <p className="section-label mb-1">Comportamento da Luna</p>
            <h1 className="text-2xl font-extrabold text-bamboo-900 flex items-center gap-3">
              <UserCircle2 className="w-7 h-7 text-bamboo-600" /> Personas
            </h1>
            <p className="text-sm text-bamboo-500 mt-0.5">Perfis de cliente que moldam como a Luna atende no Haven Escovaria</p>
          </div>
          <button onClick={() => setShowModal(true)}
            className="btn-primary flex items-center gap-2 text-sm">
            <Plus className="w-4 h-4" /> Nova Persona
          </button>
        </div>

        {/* How it works */}
        <div className="bg-gradient-to-r from-bamboo-600 to-bamboo-800 rounded-2xl p-5 text-white flex items-start gap-3 shadow-card-md">
          <Sparkles className="w-5 h-5 flex-shrink-0 mt-0.5 text-bamboo-300" />
          <div>
            <p className="font-bold text-sm">Como funciona?</p>
            <p className="text-sm text-white/80 mt-1 leading-relaxed">
              Cada persona define como a Luna deve se comportar com aquele tipo de cliente.
              Quando a IA reconhece um padrão nas mensagens (urgência, perguntas de preço, evento próximo), ela adapta o atendimento automaticamente.
            </p>
          </div>
        </div>

        {/* Personas grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          {personas.map(p => (
            <div key={p.id}
              className={`border-2 rounded-2xl p-5 cursor-pointer transition-all hover:shadow-card-md ${p.color}
                ${selected === p.id ? 'ring-2 ring-bamboo-500 ring-offset-2 shadow-card-md' : 'shadow-card'}`}
            >
              {/* Card header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{p.icon}</span>
                  <h3 className={`font-bold text-sm ${p.accent}`}>{p.name}</h3>
                </div>
                <div className="flex gap-1">
                  <button onClick={() => setSelected(selected === p.id ? null : p.id)}
                    className="w-6 h-6 rounded-lg hover:bg-white/50 flex items-center justify-center text-current opacity-50 hover:opacity-100">
                    {selected === p.id ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  </button>
                  {!DEFAULTS.some(d => d.id === p.id) && (
                    <button onClick={() => deletePersona(p.id)}
                      className="w-6 h-6 rounded-lg hover:bg-red-100 flex items-center justify-center text-red-400 hover:text-red-600">
                      <Trash2 className="w-3 h-3" />
                    </button>
                  )}
                </div>
              </div>

              <p className="text-sm text-bamboo-700 mb-3 leading-relaxed">{p.description}</p>

              <div className="flex flex-wrap gap-1.5 mb-3">
                {p.tags.map(tag => (
                  <span key={tag} className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${p.badge}`}>{tag}</span>
                ))}
              </div>

              {selected === p.id && (
                <div className="border-t border-black/10 pt-3 mt-1 space-y-1.5">
                  <p className="text-[10px] font-bold uppercase tracking-widest text-bamboo-500">Como a Luna age:</p>
                  {p.triggers.map(t => (
                    <div key={t} className="flex items-start gap-2">
                      <Target className="w-3 h-3 text-bamboo-400 mt-0.5 flex-shrink-0" />
                      <span className="text-xs text-bamboo-700">{t}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* ICP — Perfil Ideal do Haven Escovaria */}
        <div className="card-md p-6">
          <h2 className="font-bold text-bamboo-900 mb-4 flex items-center gap-2 text-sm">
            <TrendingUp className="w-5 h-5 text-bamboo-600" />
            Perfil Ideal de Cliente — Haven Escovaria (ICP)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { label: 'Frequência Ideal', value: 'Semanal', sub: 'Escova toda semana → ~R$1.4k/ano em LTV', icon: Clock },
              { label: 'Serviço Âncora', value: 'Escova', sub: 'Mais solicitado — alavanca outros serviços', icon: ShoppingBag },
              { label: 'Canal de Entrada', value: 'WhatsApp', sub: 'Principal canal de contato e agendamento', icon: MessageCircle },
            ].map(kpi => (
              <div key={kpi.label} className="bg-bamboo-50 border border-bamboo-100 rounded-xl p-4 shadow-card">
                <kpi.icon className="w-5 h-5 text-bamboo-500 mb-2" />
                <p className="text-xl font-extrabold text-bamboo-900">{kpi.value}</p>
                <p className="text-xs text-bamboo-600 font-semibold">{kpi.label}</p>
                <p className="text-[10px] text-bamboo-400 mt-0.5">{kpi.sub}</p>
              </div>
            ))}
          </div>
          <p className="text-xs text-bamboo-400 mt-4 flex items-center gap-1">
            <Sparkles className="w-3 h-3" />
            Gerado com base nos padrões reais do Haven Escovaria + PROCEDIMENTOS_HAVEN.md
          </p>
        </div>

      </div>

      {showModal && <NewPersonaModal onClose={() => setShowModal(false)} onCreated={handleCreated} />}
    </div>
  )
}
