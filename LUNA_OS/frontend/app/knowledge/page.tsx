"use client"

import { useState } from 'react'
import useSWR from 'swr'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Brain,
  Plus,
  Search,
  Trash2,
  Edit2,
  ShieldCheck,
  Scissors,
  Users,
  HelpCircle,
  AlertCircle
} from 'lucide-react'

interface KnowledgeItem {
  id: string
  category: 'service' | 'professional' | 'rule' | 'faq'
  title: string
  description: string | null
  price: number | null
  duration_minutes: number | null
  is_active: boolean
  tenant_id: string
}

const fetcher = (url: string) => fetch(url).then(res => res.json())

function Toast({ message, type, onClose }: { message: string, type: 'success' | 'error' | 'info', onClose: () => void }) {
  // eslint-disable-next-line react-hooks/exhaustive-deps
  import('react').then((React) => {
    React.useEffect(() => {
      const timer = setTimeout(onClose, 3000)
      return () => clearTimeout(timer)
    }, [onClose])
  })

  return (
    <motion.div
      initial={{ opacity: 0, y: 50, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9, y: 20 }}
      className={`fixed bottom-8 right-8 z-[100] px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3 border backdrop-blur-md ${type === 'success' ? 'bg-emerald-500/90 text-white border-emerald-400' :
          type === 'error' ? 'bg-red-500/90 text-white border-red-400' :
            'bg-gray-900/90 text-white border-gray-800'
        }`}
    >
      {type === 'success' ? <ShieldCheck className="w-5 h-5" /> : type === 'error' ? <AlertCircle className="w-5 h-5" /> : <Brain className="w-5 h-5 animate-pulse" />}
      <span className="font-bold text-sm tracking-tight">{message}</span>
    </motion.div>
  )
}

export default function KnowledgeBase() {
  const [activeTab, setActiveTab] = useState<'service' | 'professional' | 'rule' | 'faq'>('service')
  const [searchTerm, setSearchTerm] = useState('')

  // UX States
  const [toast, setToast] = useState<{ msg: string, type: 'success' | 'error' | 'info' } | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isSaving, setIsSaving] = useState(false)

  // Form State
  const [formData, setFormData] = useState<Partial<KnowledgeItem>>({
    title: '', description: '', price: 0, duration_minutes: 0, is_active: true
  })
  const [editingId, setEditingId] = useState<string | null>(null)

  const { data: items, error, isLoading, mutate } = useSWR<KnowledgeItem[]>('/api/knowledge', fetcher)

  const tabs = [
    { id: 'service', label: 'Serviços & Preços', icon: Scissors, color: 'text-luna_pink-500 bg-luna_pink-50' },
    { id: 'professional', label: 'Time', icon: Users, color: 'text-indigo-500 bg-indigo-50' },
    { id: 'rule', label: 'Regras do Salão', icon: ShieldCheck, color: 'text-emerald-500 bg-emerald-50' },
    { id: 'faq', label: 'Dúvidas e FAQ', icon: HelpCircle, color: 'text-amber-500 bg-amber-50' },
  ] as const

  const filteredItems = items?.filter(item =>
    item.category === activeTab &&
    (item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.description?.toLowerCase().includes(searchTerm.toLowerCase()))
  ) || []

  // Handlers
  const handleOpenModal = (item?: KnowledgeItem) => {
    if (item) {
      setEditingId(item.id)
      setFormData(item)
    } else {
      setEditingId(null)
      setFormData({ title: '', description: '', price: 0, duration_minutes: 0, is_active: true, category: activeTab })
    }
    setIsModalOpen(true)
  }

  const handleDelete = async (id: string, title: string) => {
    if (!window.confirm(`Tem certeza que deseja apagar "${title}"?`)) return

    try {
      await fetch(`/api/knowledge/${id}`, { method: 'DELETE' })
      setToast({ msg: 'Memória apagada com sucesso.', type: 'success' })
      mutate()
    } catch (e) {
      setToast({ msg: 'Falha ao apagar memória.', type: 'error' })
    }
  }

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSaving(true)
    try {
      const url = editingId ? `/api/knowledge/${editingId}` : '/api/knowledge'
      const method = editingId ? 'PUT' : 'POST'

      const payload = { ...formData, category: activeTab }

      await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      setToast({ msg: 'Memória neural treinada com sucesso!', type: 'success' })
      setIsModalOpen(false)
      mutate()
    } catch (e) {
      setToast({ msg: 'Falha ao sincronizar com LUNA Core.', type: 'error' })
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-[var(--color-bg)] transition-colors duration-500 relative">
      <AnimatePresence>
        {toast && <Toast message={toast.msg} type={toast.type} onClose={() => setToast(null)} />}
      </AnimatePresence>

      <div className="max-w-7xl mx-auto space-y-10">

        {/* Header */}
        <div className="flex items-end justify-between">
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
            <div className="flex items-center gap-2 mb-2">
              <span className="h-px w-8 bg-emerald-500" />
              <p className="text-[10px] font-black uppercase tracking-[0.2em] text-emerald-500">MCT Neural Core</p>
            </div>
            <h1 className="text-5xl font-black text-gray-950 tracking-tighter">Knowledge Base</h1>
            <p className="text-gray-600 mt-2 text-sm font-medium">
              Gerencie o cérebro da Luna. Defina os serviços, preços, equipe e regras do salão.
            </p>
          </motion.div>

          <motion.button
            onClick={() => handleOpenModal()}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center gap-2 bg-gray-950 text-white px-6 py-3 rounded-2xl font-bold shadow-lg shadow-gray-900/20"
          >
            <Plus className="w-5 h-5" />
            Adicionar Memória
          </motion.button>
        </div>

        {/* Categories / Tabs */}
        <div className="flex flex-wrap items-center gap-4">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-3 px-6 py-4 rounded-2xl font-bold transition-all border
                ${activeTab === tab.id
                  ? 'bg-white border-gray-200 shadow-sm text-gray-950 scale-105 relative z-10'
                  : 'bg-transparent border-transparent text-gray-500 hover:bg-white/50 hover:text-gray-800'
                }
              `}
            >
              <div className={`w-8 h-8 rounded-xl flex items-center justify-center ${tab.color}`}>
                <tab.icon className="w-4 h-4" />
              </div>
              {tab.label}

              {/* Badge Count */}
              {items && (
                <span className="ml-2 bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md text-xs">
                  {items.filter(i => i.category === tab.id).length}
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Content Area */}
        <div className="bg-white border border-gray-100 rounded-[2.5rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden p-8">

          {/* Toolbar */}
          <div className="flex items-center justify-between mb-8">
            <div className="relative w-full max-w-md">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder={`Buscar em ${tabs.find(t => t.id === activeTab)?.label}...`}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-gray-50 border-none rounded-2xl py-3 pl-12 pr-4 text-sm font-medium focus:ring-2 focus:ring-luna_pink-500 outline-none transition-all placeholder:text-gray-400"
              />
            </div>
          </div>

          {/* List */}
          <div className="space-y-4">
            {isLoading ? (
              <div className="flex flex-col items-center justify-center py-20 text-gray-400">
                <Brain className="w-10 h-10 animate-pulse mb-4 text-luna_pink-300" />
                <p className="font-bold">Acessando memórias neurais...</p>
              </div>
            ) : filteredItems.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-20 text-center">
                <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4">
                  <AlertCircle className="w-8 h-8 text-gray-300" />
                </div>
                <h3 className="text-xl font-black text-gray-800 tracking-tight">Vazio por aqui</h3>
                <p className="text-gray-500 font-medium mt-2 max-w-sm">
                  A Luna ainda não possui {tabs.find(t => t.id === activeTab)?.label.toLowerCase()} cadastrados. Adicione memórias para ensiná-la.
                </p>
              </div>
            ) : (
              <AnimatePresence>
                {filteredItems.map((item, i) => (
                  <motion.div
                    key={item.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ delay: i * 0.05 }}
                    className="group flex flex-col sm:flex-row sm:items-center gap-6 p-6 rounded-3xl border border-gray-100 hover:border-luna_pink-200 hover:bg-luna_pink-50/30 transition-all bg-white shadow-sm hover:shadow-md"
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1">
                        <h3 className="text-lg font-black text-gray-900 group-hover:text-luna_pink-700 transition-colors">{item.title}</h3>
                        {!item.is_active && (
                          <span className="px-2 py-0.5 rounded-md bg-gray-100 text-gray-500 text-[10px] font-bold uppercase tracking-widest">Inativo</span>
                        )}
                      </div>
                      <p className="text-sm font-medium text-gray-600 line-clamp-2">{item.description || 'Sem descrição inserida.'}</p>
                    </div>

                    <div className="flex items-center gap-6 sm:pl-6 sm:border-l border-gray-100">
                      {item.category === 'service' && (
                        <>
                          <div className="text-right">
                            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Preço Base</p>
                            <p className="text-lg font-black text-gray-900 line-clamp-1">{item.price ? `R$ ${item.price.toFixed(2)}` : 'Variável'}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Duração</p>
                            <p className="text-lg font-bold text-gray-700">{item.duration_minutes ? `${item.duration_minutes}m` : '---'}</p>
                          </div>
                        </>
                      )}

                      <div className="flex items-center gap-2 ml-4">
                        <button onClick={() => handleOpenModal(item)} className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-colors">
                          <Edit2 className="w-5 h-5" />
                        </button>
                        <button onClick={() => handleDelete(item.id, item.title)} className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-colors">
                          <Trash2 className="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            )}
          </div>
        </div>

      </div>

      {/* ── Modal Add / Edit ──────────────────────── */}
      <AnimatePresence>
        {isModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              onClick={() => setIsModalOpen(false)}
              className="absolute inset-0 bg-gray-950/40 backdrop-blur-sm"
            />

            {/* Modal Box */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }} animate={{ opacity: 1, scale: 1, y: 0 }} exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="relative w-full max-w-lg bg-white rounded-[2.5rem] shadow-2xl overflow-hidden"
            >
              <div className="px-8 py-6 border-b border-gray-100 bg-gray-50/50">
                <h2 className="text-2xl font-black text-gray-900 tracking-tight">
                  {editingId ? 'Editar Memória' : 'Nova Memória'}
                </h2>
                <p className="text-sm font-medium text-gray-500 mt-1">Treinando LUNA no segmento <strong className="text-luna_pink-500">{tabs.find(t => t.id === activeTab)?.label}</strong></p>
              </div>

              <form onSubmit={handleSave} className="p-8 space-y-5">
                <div>
                  <label className="block text-[11px] font-black uppercase tracking-widest text-gray-400 mb-2">Título / Nome</label>
                  <input required type="text" value={formData.title} onChange={e => setFormData({ ...formData, title: e.target.value })}
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-luna_pink-500 outline-none transition-all"
                    placeholder="Ex: Escova Modeladora"
                  />
                </div>

                <div>
                  <label className="block text-[11px] font-black uppercase tracking-widest text-gray-400 mb-2">Descrição Lógica</label>
                  <textarea rows={3} value={formData.description || ''} onChange={e => setFormData({ ...formData, description: e.target.value })}
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-luna_pink-500 outline-none transition-all custom-scrollbar"
                    placeholder="Instruções para LUNA saber quando recomendar este serviço..."
                  />
                </div>

                {activeTab === 'service' && (
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-[11px] font-black uppercase tracking-widest text-gray-400 mb-2">Preço (R$)</label>
                      <input type="number" step="0.01" value={formData.price || ''} onChange={e => setFormData({ ...formData, price: parseFloat(e.target.value) })}
                        className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-luna_pink-500 outline-none transition-all"
                      />
                    </div>
                    <div>
                      <label className="block text-[11px] font-black uppercase tracking-widest text-gray-400 mb-2">Duração (Min)</label>
                      <input type="number" value={formData.duration_minutes || ''} onChange={e => setFormData({ ...formData, duration_minutes: parseInt(e.target.value) })}
                        className="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm font-medium focus:ring-2 focus:ring-luna_pink-500 outline-none transition-all"
                      />
                    </div>
                  </div>
                )}

                <div className="pt-6 border-t border-gray-100 flex items-center justify-end gap-3">
                  <button type="button" onClick={() => setIsModalOpen(false)} className="px-5 py-2.5 text-sm font-bold text-gray-500 hover:bg-gray-50 rounded-xl transition-colors">
                    Cancelar
                  </button>
                  <button type="submit" disabled={isSaving} className="px-5 py-2.5 text-sm font-bold text-white bg-gray-950 hover:bg-gray-800 shadow-lg shadow-gray-900/10 rounded-xl transition-colors disabled:opacity-50 flex items-center gap-2">
                    {isSaving ? <Brain className="w-4 h-4 animate-pulse" /> : <ShieldCheck className="w-4 h-4" />}
                    {isSaving ? 'Sincronizando...' : 'Confirmar'}
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

    </div>
  )
}
