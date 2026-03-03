'use client'

import { useState, useEffect } from 'react'
import { AlertCircle, CheckCircle, RefreshCw, Wifi, WifiOff, Smartphone } from 'lucide-react'

export default function WhatsAppPage() {
  const [loading, setLoading] = useState(true)
  const [connecting, setConnecting] = useState(false)
  const [instanceStatus, setInstanceStatus] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    checkStatus()
  }, [])

  async function checkStatus() {
    try {
      setLoading(true)
      const res = await fetch('/api/evolution/instance/fetchInstances')
      const instances = await res.json()
      const haven = Array.isArray(instances) ? instances.find((i: any) => i.instance === 'haven') : null
      setInstanceStatus(haven ? { status: haven.status?.state || 'close' } : { status: null })
    } catch (e) {
      setError('Erro ao verificar status')
    } finally {
      setLoading(false)
    }
  }

  async function connect() {
    try {
      setConnecting(true)
      setError(null)
      const res = await fetch('/api/evolution/instance/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instanceName: 'haven', qrcode: true })
      })
      if (!res.ok) throw new Error('Erro ao criar instância')
      
      const qrRes = await fetch('/api/evolution/connect/haven', { method: 'POST' })
      if (qrRes.ok) {
        const qrData = await qrRes.json()
        setInstanceStatus({ status: 'connecting', qrcode: qrData.base64 })
      }
    } catch (e: any) {
      setError(e.message)
    } finally {
      setConnecting(false)
    }
  }

  if (loading) return <div className="flex items-center justify-center h-full"><RefreshCw className="w-12 h-12 animate-spin text-luna-600"/></div>

  return (
    <div className="space-y-6">
      <div><h1 className="text-3xl font-bold">WhatsApp</h1><p className="text-gray-600">Gerencie a conexão</p></div>
      
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h2 className="text-lg font-semibold mb-4">Status</h2>
        <div className="flex items-center space-x-4 mb-6">
          {instanceStatus?.status === 'open' ? (
            <><CheckCircle className="w-12 h-12 text-green-500"/><div><p className="font-semibold text-green-600">Conectado</p></div></>
          ) : instanceStatus?.status === 'connecting' ? (
            <><RefreshCw className="w-12 h-12 animate-spin text-yellow-500"/><div><p className="font-semibold text-yellow-600">Conectando...</p></div></>
          ) : (
            <><WifiOff className="w-12 h-12 text-red-500"/><div><p className="font-semibold text-red-600">Desconectado</p></div></>
          )}
        </div>

        {instanceStatus?.status === 'connecting' && instanceStatus?.qrcode && (
          <div className="mb-6 p-4 bg-gray-50 rounded-lg text-center">
            <img src={`data:image/png;base64,${instanceStatus.qrcode}`} alt="QR" className="mx-auto w-64 h-64"/>
          </div>
        )}

        <div className="flex space-x-4">
          {instanceStatus?.status !== 'open' ? (
            <button onClick={connect} disabled={connecting} className="px-4 py-2 bg-luna-600 text-white rounded-lg hover:bg-luna-700 disabled:opacity-50">
              <Smartphone className="w-5 h-5 inline mr-2"/>{connecting ? 'Conectando...' : 'Conectar WhatsApp'}
            </button>
          ) : null}
          <button onClick={checkStatus} className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">
            <RefreshCw className="w-5 h-5 inline mr-2"/>Atualizar
          </button>
        </div>
      </div>

      {error && <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-lg"><AlertCircle className="w-5 h-5 text-red-400 inline mr-2"/><span className="text-red-700">{error}</span></div>}
      
      <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-lg">
        <h3 className="font-semibold text-blue-800">Como conectar:</h3>
        <ol className="text-blue-700 text-sm mt-2 space-y-1">
          <li>1. Clique em "Conectar WhatsApp"</li>
          <li>2. Escaneie o QR Code no WhatsApp: Configurações → Aparelhos conectados</li>
          <li>3. Aguarde a confirmação</li>
        </ol>
      </div>
    </div>
  )
}
