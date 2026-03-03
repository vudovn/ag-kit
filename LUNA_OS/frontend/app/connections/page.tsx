"use client";

import { useState } from 'react'
import { RefreshCw, ExternalLink, Maximize2, Minimize2 } from 'lucide-react'

const EVOLUTION_MANAGER_URL = 'http://localhost:8081/manager'

export default function ConnectionsPage() {
  const [fullscreen, setFullscreen] = useState(false)
  const [reloadKey, setReloadKey] = useState(0)

  return (
    <div className={`flex flex-col transition-all duration-300 ${
      fullscreen 
        ? 'fixed inset-0 z-50 bg-gray-100' 
        : 'h-[calc(100vh-8rem)]'
    }`}>
      {/* Topbar */}
      <div className="flex items-center justify-between px-4 py-3 bg-white border-b border-gray-100 shadow-sm flex-shrink-0 rounded-t-2xl">
        <div className="flex items-center gap-3">
          <div className="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse" />
          <span className="font-bold text-gray-900 text-sm">Evolution API Manager</span>
          <span className="text-[10px] text-gray-400 bg-gray-100 px-2 py-0.5 rounded-full font-mono uppercase tracking-widest">localhost:8081</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setReloadKey(k => k + 1)}
            title="Recarregar"
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors text-gray-500 hover:text-gray-900"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
          <a
            href={EVOLUTION_MANAGER_URL}
            target="_blank"
            rel="noopener noreferrer"
            title="Abrir em nova aba"
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors text-gray-500 hover:text-gray-900"
          >
            <ExternalLink className="w-4 h-4" />
          </a>
          <button
            onClick={() => setFullscreen(f => !f)}
            title={fullscreen ? "Sair do fullscreen" : "Fullscreen"}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors text-gray-500 hover:text-gray-900"
          >
            {fullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Iframe */}
      <iframe
        key={reloadKey}
        src={EVOLUTION_MANAGER_URL}
        title="Evolution API Manager"
        className="flex-1 w-full border-0 bg-white rounded-b-2xl"
        allow="*"
        sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-modals allow-downloads"
      />
    </div>
  )
}
