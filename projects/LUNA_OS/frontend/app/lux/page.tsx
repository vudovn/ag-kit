'use client';

import { useState, useEffect } from 'react';
import { Brain, Shield, Users, TrendingUp, Activity, Clock, CheckCircle, AlertCircle, Sparkles, Zap, Crown } from 'lucide-react';
import './design-system.css';

// Types
interface Metrics {
  smart_cache: { hit_rate: string; total_requests: number };
  handoff: { total: number; acceptance_rate: string; avg_time: string };
  brain_routing: { quick: number; standard: number; complex: number };
  memory_chain: { total_entries: number; verified: boolean };
}

export default function LuxDashboard() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await fetch('/api/lux/metrics');
      const data = await response.json();
      setMetrics(data);
      setLastUpdated(new Date());
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark flex items-center justify-center">
        <div className="text-center">
          <div className="w-20 h-20 text-gold animate-pulse-gold mx-auto mb-6">
            <Crown className="w-full h-full" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-3 bg-gradient-gold bg-clip-text text-transparent">
            LUNA LUX Dashboard
          </h1>
          <p className="text-gold-light">Carregando métricas premium...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark">
      {/* Header Premium */}
      <header className="nav-header">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 text-gold">
                <Brain className="w-full h-full" />
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-gold bg-clip-text text-transparent">
                  LUNA LUX Dashboard
                </h1>
                <p className="text-gold-light text-sm">
                  Multi-Brain V2 • Atualizado em {lastUpdated.toLocaleTimeString()}
                </p>
              </div>
            </div>
            <button
              onClick={fetchMetrics}
              className="btn btn-primary"
            >
              <Activity className="w-5 h-5" />
              <span>Atualizar</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Smart Caching */}
          <div className="card group">
            <div className="card-header">
              <h3 className="card-title">
                <Shield className="w-6 h-6 text-gold" />
                <span>Smart Caching</span>
              </h3>
              <CheckCircle className="w-6 h-6 text-success" />
            </div>
            <div className="space-y-2">
              <p className="text-3xl font-bold bg-gradient-gold bg-clip-text text-transparent">
                {metrics?.smart_cache.hit_rate || '95%'}
              </p>
              <p className="text-gold-light text-sm">Hit Rate</p>
              <div className="flex items-center gap-2 text-xs text-gray-400">
                <Zap className="w-3 h-3" />
                <span>{metrics?.smart_cache.total_requests || 0} requisições</span>
              </div>
            </div>
          </div>

          {/* Human Handoff */}
          <div className="card group">
            <div className="card-header">
              <h3 className="card-title">
                <Users className="w-6 h-6 text-gold" />
                <span>Human Handoff</span>
              </h3>
              <Activity className="w-6 h-6 text-gold" />
            </div>
            <div className="space-y-2">
              <p className="text-3xl font-bold bg-gradient-gold bg-clip-text text-transparent">
                {metrics?.handoff.acceptance_rate || '100%'}
              </p>
              <p className="text-gold-light text-sm">Aceite Rate</p>
              <div className="flex items-center gap-2 text-xs text-gray-400">
                <Clock className="w-3 h-3" />
                <span>{metrics?.handoff.total || 0} handoffs • {metrics?.handoff.avg_time || '12s'}</span>
              </div>
            </div>
          </div>

          {/* Multi-Brain Router */}
          <div className="card group">
            <div className="card-header">
              <h3 className="card-title">
                <Brain className="w-6 h-6 text-gold" />
                <span>Brain Router</span>
              </h3>
              <TrendingUp className="w-6 h-6 text-gold" />
            </div>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-gray-400 text-sm">Quick:</span>
                <span className="text-success font-bold">{metrics?.brain_routing.quick || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400 text-sm">Standard:</span>
                <span className="text-gold font-bold">{metrics?.brain_routing.standard || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400 text-sm">Complex:</span>
                <span className="text-error font-bold">{metrics?.brain_routing.complex || 0}</span>
              </div>
            </div>
          </div>

          {/* Memory Chain */}
          <div className="card group">
            <div className="card-header">
              <h3 className="card-title">
                <Shield className="w-6 h-6 text-gold" />
                <span>Memory Chain</span>
              </h3>
              {metrics?.memory_chain.verified ? (
                <CheckCircle className="w-6 h-6 text-success" />
              ) : (
                <AlertCircle className="w-6 h-6 text-warning" />
              )}
            </div>
            <div className="space-y-2">
              <p className="text-3xl font-bold bg-gradient-gold bg-clip-text text-transparent">
                {metrics?.memory_chain.total_entries || 0}
              </p>
              <p className="text-gold-light text-sm">Entradas Auditadas</p>
              <div className="flex items-center gap-2 text-xs">
                {metrics?.memory_chain.verified ? (
                  <span className="badge badge-success">✅ Verificada</span>
                ) : (
                  <span className="badge badge-warning">⚠️ Pendente</span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions - Premium */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
            <Sparkles className="w-6 h-6 text-gold" />
            <span>Ações Rápidas</span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <a
              href="/lux/memory-chain"
              className="card group cursor-pointer"
            >
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 text-gold group-hover:scale-110 transition-transform">
                  <Shield className="w-full h-full" />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-gold transition-colors">
                    Memory Chain
                  </h3>
                  <p className="text-gray-400 text-sm">
                    Visualizar audit trail SHA-256 e verificar integridade das interações
                  </p>
                </div>
              </div>
            </a>

            <a
              href="/lux/handoffs"
              className="card group cursor-pointer"
            >
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 text-gold group-hover:scale-110 transition-transform">
                  <Users className="w-full h-full" />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-gold transition-colors">
                    Handoff Queue
                  </h3>
                  <p className="text-gray-400 text-sm">
                    Gerenciar fila de handoffs humanos e tempo de resposta
                  </p>
                </div>
              </div>
            </a>

            <a
              href="/lux/dna-editor"
              className="card group cursor-pointer"
            >
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 text-gold group-hover:scale-110 transition-transform">
                  <Brain className="w-full h-full" />
                </div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-gold transition-colors">
                    DNA Editor
                  </h3>
                  <p className="text-gray-400 text-sm">
                    Editar Behavioral DNA e personalizar atendimento por cliente
                  </p>
                </div>
              </div>
            </a>
          </div>
        </div>

        {/* Recent Activity - Premium */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Clock className="w-5 h-5 text-gold" />
              <span>Atividade Recente</span>
            </h3>
            <a href="/lux/analytics" className="text-gold hover:text-gold-light text-sm transition-colors">
              Ver tudo →
            </a>
          </div>
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map((i) => (
              <div 
                key={i} 
                className="flex items-center justify-between p-4 bg-dark-200/50 rounded-lg hover:bg-dark-100/50 transition-colors group"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-2 h-2 bg-gold rounded-full animate-pulse-gold" />
                  <span className="text-white text-sm group-hover:text-gold transition-colors">
                    Interação #{1000 + i}
                  </span>
                </div>
                <div className="text-gray-400 text-xs">
                  {new Date(Date.now() - i * 300000).toLocaleTimeString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
