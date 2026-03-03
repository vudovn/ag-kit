"use client";

import { useState, useEffect } from 'react'
import { Bot, Building2, Cpu, Key, Eye, EyeOff, CheckCircle, AlertCircle, Save, Loader2, RefreshCw, Wifi } from 'lucide-react'
import ConnectionStatus from '../connections/ConnectionStatus'

type Status = 'idle' | 'saving' | 'saved' | 'error'
type Tab = 'geral' | 'conexoes'

function Section({ icon: Icon, title, children }: { icon: any; title: string; children: React.ReactNode }) {
  return (
    <div className="card-md p-6">
      <div className="flex items-center gap-2.5 mb-5 pb-4 border-b border-bamboo-100">
        <div className="w-7 h-7 rounded-lg bg-bamboo-100 flex items-center justify-center">
          <Icon className="w-4 h-4 text-bamboo-600" />
        </div>
        <h2 className="font-bold text-bamboo-900 text-sm">{title}</h2>
      </div>
      {children}
    </div>
  )
}

function Field({ label, hint, children }: { label: string; hint?: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1.5 flex-1">
      <label className="block text-xs font-semibold text-bamboo-700">{label}</label>
      {children}
      {hint && <p className="text-[11px] text-bamboo-400">{hint}</p>}
    </div>
  )
}

const EVOLUTION_MANAGER_URL = process.env.NEXT_PUBLIC_EVOLUTION_MANAGER_URL || 'http://localhost:8081/manager'

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState<Tab>('geral')
  const [config, setConfig] = useState<any>(null)

  // Sovereign Switch state
  const [lunaMode, setLunaMode] = useState<'active' | 'observe'>('observe')
  const [belasisMock, setBelasisMock] = useState(true)
  const [modeStatus, setModeStatus] = useState<Status>('idle')

  // OpenRouter key state
  const [orKey, setOrKey] = useState('')
  const [orVisible, setOrVisible] = useState(false)
  const [orStatus, setOrStatus] = useState<Status>('idle')

  // Models state
  const [modelsList, setModelsList] = useState<any[]>([])
  const [modelQuick, setModelQuick] = useState('')
  const [modelStandard, setModelStandard] = useState('')
  const [modelComplex, setModelComplex] = useState('')
  const [modelsStatus, setModelsStatus] = useState<Status>('idle')

  useEffect(() => {
    // Fetch generic settings
    fetch('/api/settings')
      .then(r => r.json())
      .then(d => {
        setConfig(d)
        if (d.integrations?.openrouter_configured) {
          setOrKey('••••••••••••••••••••••••••') // masked placeholder
        }
        setModelQuick(d.ai?.models?.quick?.id || '')
        setModelStandard(d.ai?.models?.standard?.id || '')
        setModelComplex(d.ai?.models?.complex?.id || '')

        // Load operation mode
        if (d.mode) {
          setLunaMode(d.mode.luna_mode || 'observe')
          setBelasisMock(d.mode.belasis_mock !== false) // default to true if not explicitly false
        }
      })
      .catch(() => { })

    // Fetch dynamic models list
    fetch('/api/settings/openrouter-models')
      .then(r => r.json())
      .then(d => {
        setModelsList(d.data || [])
      })
      .catch(() => { })
  }, [])

  async function saveOrKey() {
    if (!orKey || orKey.startsWith('••')) {
      setOrStatus('error')
      setTimeout(() => setOrStatus('idle'), 2000)
      return
    }
    setOrStatus('saving')
    try {
      const r = await fetch('/api/settings/openrouter-key', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key: orKey }),
      })
      setOrStatus(r.ok ? 'saved' : 'error')
      if (r.ok) {
        setOrVisible(false)
        setOrKey('••••••••••••••••••••••••••')
        // Refresh models list after setting valid key
        fetch('/api/settings/openrouter-models')
          .then(r => r.json())
          .then(d => setModelsList(d.data || []))
          .catch(() => { })
      }
    } catch {
      setOrStatus('error')
    } finally {
      setTimeout(() => setOrStatus('idle'), 3000)
    }
  }

  async function saveOperationMode(newMode: 'active' | 'observe', newMock: boolean) {
    setModeStatus('saving')
    try {
      const r = await fetch('/api/settings/operation-mode', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          luna_mode: newMode,
          belasis_mock: newMock
        }),
      })
      if (r.ok) {
        setLunaMode(newMode)
        setBelasisMock(newMock)
        setModeStatus('saved')
      } else {
        setModeStatus('error')
      }
    } catch {
      setModeStatus('error')
    } finally {
      setTimeout(() => setModeStatus('idle'), 3000)
    }
  }

  async function saveModels() {
    setModelsStatus('saving')
    try {
      const r = await fetch('/api/settings/models', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model_quick: modelQuick,
          model_standard: modelStandard,
          model_complex: modelComplex
        }),
      })
      setModelsStatus(r.ok ? 'saved' : 'error')
    } catch {
      setModelsStatus('error')
    } finally {
      setTimeout(() => setModelsStatus('idle'), 3000)
    }
  }

  const orConfigured = config?.integrations?.openrouter_configured

  return (
    <div className="flex-1 flex flex-col h-full bg-bamboo-50/30 overflow-hidden">
      {/* Header Area (Sticky) */}
      <div className="flex-shrink-0 p-8 pb-0">
        <div className="max-w-4xl mx-auto">
          <p className="section-label mb-1">MCT OS Configuração Soberana</p>
          <h1 className="text-2xl font-extrabold text-bamboo-900">Configurações Gerais</h1>
          <p className="text-sm text-bamboo-500 mt-0.5">Gerencie tokens, provedores de inferência e conectividade.</p>

          {/* Tabs */}
          <div className="flex gap-2 mt-6 border-b border-bamboo-200">
            <button
              onClick={() => setActiveTab('geral')}
              className={`px-4 py-2.5 text-sm font-bold border-b-2 transition-colors ${activeTab === 'geral' ? 'border-bamboo-600 text-bamboo-700' : 'border-transparent text-bamboo-400 hover:text-bamboo-600'}`}
            >
              Geral & IA
            </button>
            <button
              onClick={() => setActiveTab('conexoes')}
              className={`px-4 py-2.5 text-sm font-bold border-b-2 flex items-center gap-2 transition-colors ${activeTab === 'conexoes' ? 'border-bamboo-600 text-bamboo-700' : 'border-transparent text-bamboo-400 hover:text-bamboo-600'}`}
            >
              <Wifi className="w-4 h-4" /> Gateway Evolution API
            </button>
          </div>
        </div>
      </div>

      {/* Main Content Area (Scrollable) */}
      <div className="flex-1 overflow-y-auto p-8 relative">
        <div className="max-w-4xl mx-auto space-y-6">

          {activeTab === 'geral' && (
            <>
              {/* ── Sovereign Switch (Controle de Produção) ──── */}
              <Section icon={Bot} title="Sovereign Switch (Modo de Operação)">
                <div className="space-y-6">
                  <div className="flex items-start gap-4 p-4 rounded-xl bg-bamboo-900 text-white shadow-lg overflow-hidden relative">
                    <div className="absolute top-0 right-0 p-1 bg-white/10 rounded-bl-xl text-[9px] font-bold tracking-widest uppercase">Kernel Control</div>
                    <div className={`p-2.5 rounded-lg ${lunaMode === 'active' && !belasisMock ? 'bg-red-500 animate-pulse' : 'bg-white/10'}`}>
                      <Building2 className="w-5 h-5" />
                    </div>
                    <div className="flex-1">
                      <p className="text-xs font-bold uppercase tracking-wider text-white/70">Estado do Sistema</p>
                      <h3 className="text-lg font-black tracking-tight mt-0.5">
                        {lunaMode === 'active'
                          ? (belasisMock ? 'LUNA EM TREINAMENTO' : 'LUNA EM PRODUÇÃO ATIVA')
                          : 'LUNA EM MODO OBSERVAÇÃO'
                        }
                      </h3>
                      <p className="text-[11px] text-white/50 mt-1 leading-relaxed">
                        {lunaMode === 'active' && !belasisMock
                          ? 'CUIDADO: Luna está respondendo clientes reais com dados da Belasis.'
                          : 'A Luna registrará conversas mas não enviará mensagens automáticas.'
                        }
                      </p>
                    </div>
                    <div className="flex flex-col gap-2">
                      <button
                        onClick={() => saveOperationMode(lunaMode === 'active' ? 'observe' : 'active', belasisMock)}
                        disabled={modeStatus === 'saving'}
                        className={`px-4 py-2 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all
                          ${lunaMode === 'active'
                            ? 'bg-red-500 hover:bg-red-600 text-white'
                            : 'bg-white/10 hover:bg-white/20 text-white'
                          }
                        `}
                      >
                        {modeStatus === 'saving' ? '...' : (lunaMode === 'active' ? 'DESATIVAR' : 'ATIVAR')}
                      </button>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 rounded-xl border border-bamboo-100 bg-white shadow-sm flex items-center justify-between">
                      <div className="space-y-0.5">
                        <p className="text-xs font-bold text-bamboo-900">Resposta Automática</p>
                        <p className="text-[10px] text-bamboo-500">Luna responde sozinha no WhatsApp</p>
                      </div>
                      <button
                        onClick={() => saveOperationMode(lunaMode === 'active' ? 'observe' : 'active', belasisMock)}
                        className={`w-12 h-6 rounded-full transition-colors relative ${lunaMode === 'active' ? 'bg-bamboo-600' : 'bg-bamboo-200'}`}
                      >
                        <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${lunaMode === 'active' ? 'left-7' : 'left-1'}`} />
                      </button>
                    </div>

                    <div className="p-4 rounded-xl border border-bamboo-100 bg-white shadow-sm flex items-center justify-between">
                      <div className="space-y-0.5">
                        <p className="text-xs font-bold text-bamboo-900">Integração Belasis</p>
                        <p className="text-[10px] text-bamboo-500">Usar dados reais da Belasis API</p>
                      </div>
                      <button
                        onClick={() => saveOperationMode(lunaMode, !belasisMock)}
                        className={`w-12 h-6 rounded-full transition-colors relative ${!belasisMock ? 'bg-bamboo-600' : 'bg-bamboo-200'}`}
                      >
                        <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${!belasisMock ? 'left-7' : 'left-1'}`} />
                      </button>
                    </div>
                  </div>
                </div>
              </Section>
              {/* ── OpenRouter API Key ─────────────────── */}
              <Section icon={Key} title="Chave Mestra de Inferência (OpenRouter)">
                <div className="space-y-4">
                  <div className="flex items-start gap-3 p-3.5 rounded-xl bg-bamboo-50 border border-bamboo-200">
                    {orConfigured ? (
                      <CheckCircle className="w-5 h-5 text-bamboo-500 flex-shrink-0 mt-0.5" />
                    ) : (
                      <AlertCircle className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
                    )}
                    <div className="text-xs">
                      <p className="font-semibold text-bamboo-800">
                        {orConfigured ? 'Gateway de inferência seguro e ativo.' : '⚠️ Chave não configurada — Luna OS operará em falha total.'}
                      </p>
                      <p className="text-bamboo-500 mt-0.5">
                        Obtenha em <a href="https://openrouter.ai/keys" target="_blank" rel="noreferrer" className="text-bamboo-600 font-bold underline underline-offset-2">openrouter.ai/keys</a>. Formato esperado: <code className="bg-bamboo-100 text-bamboo-700 font-bold px-1 rounded font-mono">sk-or-v1-...</code>
                      </p>
                    </div>
                  </div>

                  <Field label="OPENROUTER_API_KEY" hint="Token salvo no kernel (environment variables) em disco seguro.">
                    <div className="flex gap-2">
                      <div className="flex-1 relative">
                        <input
                          type={orVisible ? 'text' : 'password'}
                          value={orKey}
                          onChange={e => setOrKey(e.target.value)}
                          placeholder="sk-or-v1-..."
                          className="input-field pr-10 font-mono text-sm"
                        />
                        <button onClick={() => setOrVisible(v => !v)}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-bamboo-400 hover:text-bamboo-600">
                          {orVisible ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </button>
                      </div>
                      <button onClick={saveOrKey} disabled={orStatus === 'saving'}
                        className={`btn-primary flex items-center gap-1.5 text-sm min-w-[100px] justify-center
                          ${orStatus === 'saved' ? 'bg-bamboo-600' : ''}
                          ${orStatus === 'error' ? 'bg-red-500 hover:bg-red-600' : ''}
                        `}>
                        {orStatus === 'saving' ? <Loader2 className="w-4 h-4 animate-spin" /> :
                          orStatus === 'saved' ? <CheckCircle className="w-4 h-4" /> :
                            orStatus === 'error' ? <AlertCircle className="w-4 h-4" /> :
                              <Save className="w-4 h-4" />}
                        {orStatus === 'saved' ? 'Salvo!' : orStatus === 'error' ? 'Erro' : 'Persistir'}
                      </button>
                    </div>
                  </Field>
                </div>
              </Section>

              {/* ── Modelos de IA Dinâmicos ─────────────────────── */}
              <Section icon={Cpu} title="Matriz de Modelos Cognitivos">
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

                    <Field label="Quick Brain (Intent Engine)" hint="Altíssima latência (≤500ms). Respostas secas de roteamento. Recomendado: Haiku ou modelos compactos.">
                      <select value={modelQuick} onChange={(e) => setModelQuick(e.target.value)} className="input-field text-xs font-mono">
                        <option value="">Selecione um modelo...</option>
                        {modelsList.map(m => (
                          <option key={`quick-${m.id}`} value={m.id}>{m.name || m.id.split('/').pop()}</option>
                        ))}
                      </select>
                    </Field>

                    <Field label="Standard Brain (Conversação)" hint="Latência moderada, alto QI social. Executa vendas e agendamentos. Recomendado: Sonnet.">
                      <select value={modelStandard} onChange={(e) => setModelStandard(e.target.value)} className="input-field text-xs font-mono">
                        <option value="">Selecione um modelo...</option>
                        {modelsList.map(m => (
                          <option key={`standard-${m.id}`} value={m.id}>{m.name || m.id.split('/').pop()}</option>
                        ))}
                      </select>
                    </Field>

                    <Field label="Complex Brain (Análise Profunda)" hint="Reclamações, quebra de objeções complexas. Recomendado: R1 ou equivalente.">
                      <select value={modelComplex} onChange={(e) => setModelComplex(e.target.value)} className="input-field text-xs font-mono">
                        <option value="">Selecione um modelo...</option>
                        {modelsList.map(m => (
                          <option key={`complex-${m.id}`} value={m.id}>{m.name || m.id.split('/').pop()}</option>
                        ))}
                      </select>
                    </Field>

                  </div>

                  <div className="flex justify-end pt-2 border-t border-bamboo-100">
                    <button onClick={saveModels} disabled={modelsStatus === 'saving'}
                      className={`btn-primary flex items-center gap-1.5 text-sm min-w-[100px] justify-center
                            ${modelsStatus === 'saved' ? 'bg-bamboo-600' : ''}
                            ${modelsStatus === 'error' ? 'bg-red-500 hover:bg-red-600' : ''}
                          `}>
                      {modelsStatus === 'saving' ? <Loader2 className="w-4 h-4 animate-spin" /> :
                        modelsStatus === 'saved' ? <CheckCircle className="w-4 h-4" /> :
                          modelsStatus === 'error' ? <AlertCircle className="w-4 h-4" /> :
                            <Save className="w-4 h-4" />}
                      {modelsStatus === 'saved' ? 'Modelos Ativos!' : modelsStatus === 'error' ? 'Erro' : 'Aplicar Modelos'}
                    </button>
                  </div>
                </div>
              </Section>
            </>
          )}

          {activeTab === 'conexoes' && (
            <div className="bg-white rounded-2xl shadow-card h-[600px] border border-bamboo-100 flex flex-col overflow-hidden">
              {/* Iframe Evolution */}
              <iframe
                src={EVOLUTION_MANAGER_URL}
                title="Evolution API Manager"
                className="flex-1 w-full border-0 bg-gray-50 bg-white"
                allow="*"
                sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-modals allow-downloads"
              />
            </div>
          )}

        </div>
      </div>
    </div>
  )
}

