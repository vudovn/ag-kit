"use client";

import useSWR from 'swr';
import { motion } from 'framer-motion';
import { Scissors, Clock, DollarSign, Tag, Search, AlertCircle, ExternalLink } from 'lucide-react';
import { useState, useMemo } from 'react';

const fetcher = (url: string) => fetch(url).then(res => res.json());

const WHATSAPP_NUMBER = '554991099437';

function ServiceSkeleton() {
  return (
    <div className="card-md p-6 animate-pulse">
      <div className="h-6 bg-luna_pink-100 rounded-xl w-3/4 mb-4" />
      <div className="space-y-2">
        <div className="h-4 bg-luna_pink-50 rounded w-1/2" />
        <div className="h-4 bg-luna_pink-50 rounded w-1/3" />
      </div>
    </div>
  );
}

export default function ServicesPage() {
  const { data, error, isLoading } = useSWR('/api/services', fetcher);
  const [search, setSearch] = useState('');

  const services = data?.services || [];

  const servicesByCategory = useMemo(() => {
    const filtered = search
      ? services.filter((s: any) => s.name?.toLowerCase().includes(search.toLowerCase()))
      : services;

    return filtered.reduce((acc: any, service: any) => {
      const category = service.category || 'outros';
      if (!acc[category]) acc[category] = [];
      acc[category].push(service);
      return acc;
    }, {});
  }, [services, search]);

  const categoryLabels: Record<string, string> = {
    cabelo: '💇‍♀️ Cabelo',
    unha: '💅 Unhas',
    maquiagem: '💄 Maquiagem',
    depilacao: '🪒 Depilação',
    sobrancelha: '✨ Sobrancelha',
    outros: '📌 Outros',
  };

  function handleAgendar(serviceName: string) {
    const msg = encodeURIComponent(`Oi! Gostaria de agendar: ${serviceName}`);
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${msg}`, '_blank');
  }

  if (error) return <div className="p-8 text-red-600">Erro ao carregar serviços</div>;

  return (
    <div className="flex-1 overflow-y-auto bg-[var(--color-bg)] p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <p className="section-label mb-1">Catálogo Haven</p>
          <h1 className="text-3xl font-black text-gray-900 mb-2">Serviços</h1>
          <p className="text-sm text-gray-500">Todos os serviços e valores da Haven Escovaria</p>
        </div>

        {/* Search */}
        <div className="relative mb-8 max-w-md">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-luna_pink-400" />
          <input
            type="text"
            placeholder="Buscar serviço..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input-field pl-10"
          />
        </div>

        {isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {[...Array(6)].map((_, i) => <ServiceSkeleton key={i} />)}
          </div>
        )}

        {!isLoading && Object.entries(servicesByCategory).map(([category, categoryServices]: [string, any]) => (
          <div key={category} className="mb-10">
            <h2 className="text-lg font-black text-gray-900 mb-4">{categoryLabels[category] || category}</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {categoryServices.map((service: any, i: number) => (
                <motion.div
                  key={service.key}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className="card-md p-6 hover:shadow-card-lg transition-all group"
                >
                  <h3 className="text-base font-black text-gray-900 mb-3">{service.name}</h3>

                  {service.alert && (
                    <div className="flex items-start gap-2 p-2.5 mb-3 rounded-xl bg-amber-50 border border-amber-200">
                      <AlertCircle className="w-3.5 h-3.5 text-amber-500 mt-0.5 flex-shrink-0" />
                      <p className="text-[11px] text-amber-700 font-medium">{service.alert}</p>
                    </div>
                  )}

                  <div className="space-y-2.5 mb-4">
                    <div className="flex items-center gap-2">
                      <DollarSign className="w-4 h-4 text-luna_pink-500" />
                      <span className="text-lg font-black text-luna_pink-600">
                        R$ {service.price?.toFixed(2) || service.price_min?.toFixed(2)}
                        {service.price_max && (
                          <span className="text-sm text-gray-500 font-medium"> a R$ {service.price_max.toFixed(2)}</span>
                        )}
                      </span>
                    </div>
                    {service.promo_price_seg_qua && (
                      <p className="text-[11px] text-luna_pink-500 font-bold bg-luna_pink-50 px-2 py-1 rounded-lg inline-block">
                        🏷️ Promo Seg-Qua: R$ {service.promo_price_seg_qua.toFixed(2)}
                      </p>
                    )}
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Clock className="w-3.5 h-3.5 text-gray-400" />
                      <span className="font-medium">{service.duration_min} min</span>
                    </div>
                    {service.professionals && (
                      <div className="flex items-center gap-2 text-[11px] text-gray-500">
                        <Tag className="w-3 h-3 text-gray-400" />
                        <span>{service.professionals.join(', ')}</span>
                      </div>
                    )}
                    {service.includes_blowdry !== undefined && (
                      <p className={`text-[11px] font-bold ${service.includes_blowdry ? 'text-emerald-600' : 'text-gray-400'}`}>
                        {service.includes_blowdry ? '✅ Inclui escova' : '⬜ Escova não inclusa'}
                      </p>
                    )}
                  </div>

                  <button
                    onClick={() => handleAgendar(service.name)}
                    className="btn-primary w-full flex items-center justify-center gap-2 text-sm"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    Agendar via WhatsApp
                  </button>
                </motion.div>
              ))}
            </div>
          </div>
        ))}

        {!isLoading && services.length === 0 && (
          <div className="text-center py-16">
            <Scissors className="w-16 h-16 text-luna_pink-200 mx-auto mb-4" />
            <p className="text-gray-500 font-medium">Nenhum serviço encontrado</p>
          </div>
        )}
      </div>
    </div>
  );
}
