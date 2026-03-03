"use client";

import React from 'react';
import { CheckCircle, AlertCircle, RefreshCw, Database, Cpu, Share2, LucideIcon } from 'lucide-react';

interface StatusItemProps {
  label: string;
  status: 'connected' | 'warning' | 'error' | 'not_configured' | 'disconnected' | 'unknown';
  icon: LucideIcon;
  details?: string;
  latency?: number;
}

function StatusItem({ label, status, icon: Icon, details, latency }: StatusItemProps) {
  const statusColors = {
    connected: 'text-bamboo-600 bg-bamboo-50 border-bamboo-200',
    warning: 'text-amber-600 bg-amber-50 border-amber-200',
    error: 'text-red-600 bg-red-50 border-red-200',
    not_configured: 'text-gray-500 bg-gray-50 border-gray-200',
    disconnected: 'text-red-700 bg-red-100 border-red-300',
    unknown: 'text-gray-400 bg-gray-50 border-gray-100'
  };

  const statusIcons: Record<string, React.ReactNode> = {
    connected: <CheckCircle className="w-4 h-4" />,
    warning: <AlertCircle className="w-4 h-4" />,
    error: <AlertCircle className="w-4 h-4" />,
    not_configured: <AlertCircle className="w-4 h-4" />,
    disconnected: <AlertCircle className="w-4 h-4" />,
    unknown: <AlertCircle className="w-4 h-4 opacity-50" />
  };

  const statusLabels: Record<string, string> = {
    connected: 'Sincronizado',
    warning: 'Atenção',
    error: 'Erro',
    not_configured: 'Não Configurado',
    disconnected: 'Desconectado',
    unknown: 'Verificando...'
  };

  return (
    <div className={`p-3 rounded-xl border flex items-center justify-between transition-all ${statusColors[status]}`}>
      <div className="flex items-center gap-3">
        <div className={`p-2 rounded-lg ${status === 'connected' ? 'bg-white/50' : 'bg-white/80'}`}>
          <Icon className="w-4 h-4" />
        </div>
        <div>
          <p className="text-xs font-bold">{label}</p>
          <div className="flex items-center gap-1.5 mt-0.5">
            <span className="text-[10px] font-medium uppercase tracking-wider opacity-80">{statusLabels[status]}</span>
            {latency !== undefined && latency > 0 && (
              <span className="text-[9px] px-1 rounded bg-black/5 font-mono">{latency}ms</span>
            )}
          </div>
          {details && (
            <p className="text-[9px] mt-1 italic opacity-70 truncate max-w-[150px]">{details}</p>
          )}
        </div>
      </div>
      <div className="flex items-center gap-2">
         {statusIcons[status]}
      </div>
    </div>
  );
}

interface ServiceStatus {
  status: string;
  details?: string;
  latency?: number;
}

interface HealthStatus {
  last_check: string;
  overall: 'healthy' | 'attention' | 'unhealthy';
  supabase: ServiceStatus;
  openrouter: ServiceStatus;
  evolution: ServiceStatus;
  system?: ServiceStatus;
}

export default function ConnectionStatus({ 
  health, 
  onRefresh, 
  loading 
}: { 
  health: HealthStatus | null, 
  onRefresh: () => void, 
  loading: boolean 
}) {
  if (!health) return null;

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between px-1">
        <p className="text-[10px] font-bold text-bamboo-400 uppercase tracking-widest flex items-center gap-2">
          <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} onClick={() => onRefresh()} />
          Soberania de Conexão {health.last_check && `• ÚLTIMA ATUALIZAÇÃO: ${health.last_check}`}
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        <StatusItem 
          label="Supabase (Brain)" 
          status={health.supabase.status as any} 
          icon={Database}
          latency={health.supabase.latency}
          details={health.supabase.details}
        />
        <StatusItem 
          label="OpenRouter (IA)" 
          status={health.openrouter.status as any} 
          icon={Cpu}
          details={health.openrouter.details}
        />
        <StatusItem 
          label="Evolution (WhatsApp)" 
          status={health.evolution.status as any} 
          icon={Share2}
          details={health.evolution.details}
        />
        <StatusItem 
          label="Servidor (Infra)" 
          status={(health.system?.status || 'unknown') as any} 
          icon={Database}
          details={health.system?.details}
        />
      </div>
      
      {health.overall === 'unhealthy' && (
        <div className="p-2.5 rounded-lg border border-red-200 bg-red-50 flex items-center gap-3 text-red-700">
           <AlertCircle className="w-4 h-4 shrink-0" />
           <p className="text-xs font-medium">Atenção: A LUNA pode apresentar instabilidade ou silêncio operacional devido a falhas críticas abaixo.</p>
        </div>
      )}
    </div>
  );
}
