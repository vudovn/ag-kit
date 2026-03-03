"use client";

import useSWR from 'swr';
import { motion } from 'framer-motion';
import { Package, Clock, DollarSign, Calendar, ExternalLink, ShieldCheck } from 'lucide-react';

const fetcher = (url: string) => fetch(url).then(res => res.json());

const WHATSAPP_NUMBER = '554991099437';

function PackageSkeleton() {
  return (
    <div className="card-md p-6 animate-pulse">
      <div className="flex items-start gap-4 mb-4">
        <div className="w-16 h-16 rounded-2xl bg-luna_pink-100" />
        <div className="flex-1 space-y-2">
          <div className="h-6 bg-luna_pink-100 rounded w-3/4" />
          <div className="h-3 bg-luna_pink-50 rounded w-1/2" />
        </div>
      </div>
      <div className="space-y-3">
        <div className="h-4 bg-luna_pink-50 rounded w-full" />
        <div className="h-20 bg-luna_pink-50 rounded w-full" />
      </div>
    </div>
  );
}

export default function PackagesPage() {
  const { data, error, isLoading } = useSWR('/api/packages', fetcher);

  if (error) return <div className="p-8 text-red-600">Erro ao carregar pacotes</div>;

  const packages = data?.packages || [];

  function handleComprar(name: string) {
    const msg = encodeURIComponent(`Oi! Tenho interesse no ${name}. Podem me dar mais informações?`);
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${msg}`, '_blank');
  }

  return (
    <div className="flex-1 overflow-y-auto bg-[var(--color-bg)] p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <p className="section-label mb-1">Catálogo Haven</p>
          <h1 className="text-3xl font-black text-gray-900 mb-2">Pacotes</h1>
          <p className="text-sm text-gray-500">Economize com nossos pacotes promocionais</p>
        </div>

        {isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[...Array(4)].map((_, i) => <PackageSkeleton key={i} />)}
          </div>
        )}

        {!isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {packages.map((pkg: any, index: number) => {
              const avulsoPrice = pkg.type === 'gel_maos' ? 80 : 59;
              const pkgPrice = pkg.type === 'gel_maos' ? pkg.price_lu : pkg.price_lisa;
              const economy = pkgPrice ? ((avulsoPrice * pkg.quantity) - (pkgPrice * pkg.quantity)) : 0;

              return (
                <motion.div
                  key={pkg.key}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="card-md p-6 hover:shadow-card-lg transition-all border-2 border-luna_pink-100 relative overflow-hidden"
                >
                  {economy > 0 && (
                    <div className="absolute top-4 right-4 bg-gradient-to-r from-luna_pink-500 to-purple-500 text-white text-[10px] font-black px-3 py-1 rounded-full shadow-lg">
                      ECONOMIZE R$ {economy.toFixed(0)}
                    </div>
                  )}

                  <div className="flex items-start gap-4 mb-5">
                    <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-luna_pink-400 to-purple-500 flex items-center justify-center text-white flex-shrink-0 shadow-sm">
                      <Package className="w-7 h-7" />
                    </div>
                    <div className="flex-1">
                      <h2 className="text-xl font-black text-gray-900 mb-1">{pkg.name}</h2>
                      <div className="flex items-center gap-2">
                        <Calendar className="w-3.5 h-3.5 text-gray-400" />
                        <span className="text-xs font-medium text-gray-500">Validade: {pkg.validity_days} dias</span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4 mb-5">
                    <div>
                      <div className="flex items-center gap-1.5 mb-2">
                        <DollarSign className="w-3.5 h-3.5 text-luna_pink-500" />
                        <p className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Valores</p>
                      </div>
                      {pkg.type === 'gel_maos' && (
                        <div className="space-y-1">
                          <p className="text-lg font-black text-luna_pink-600">
                            Lu: R$ {pkg.price_lu?.toFixed(2)} <span className="text-sm font-medium text-gray-400">cada</span>
                          </p>
                          <p className="text-lg font-black text-luna_pink-600">
                            Dávila: R$ {pkg.price_davila?.toFixed(2)} <span className="text-sm font-medium text-gray-400">cada</span>
                          </p>
                        </div>
                      )}
                      {pkg.type === 'escovas' && (
                        <div className="space-y-1">
                          <p className="text-lg font-black text-luna_pink-600">
                            Lisa: R$ {pkg.price_lisa?.toFixed(2)} <span className="text-sm font-medium text-gray-400">cada</span>
                          </p>
                          <p className="text-lg font-black text-luna_pink-600">
                            Modelada: R$ {pkg.price_modelada?.toFixed(2)} <span className="text-sm font-medium text-gray-400">cada</span>
                          </p>
                        </div>
                      )}
                      <p className="text-xs text-gray-500 mt-2 font-bold">
                        📦 {pkg.quantity} aplicações no total
                      </p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-luna_pink-50 border border-luna_pink-100">
                      <div className="flex items-center gap-1.5 mb-2">
                        <ShieldCheck className="w-3.5 h-3.5 text-luna_pink-500" />
                        <p className="text-[10px] font-bold text-luna_pink-600 uppercase tracking-wider">Regras do Pacote</p>
                      </div>
                      <ul className="text-[11px] text-gray-600 space-y-1 leading-relaxed">
                        <li>• Somente à vista (Pix ou dinheiro)</li>
                        <li>• Não parcelamos pacotes</li>
                        <li>• Validade: {pkg.validity_days} dias</li>
                        <li>• Agendamento necessário para cada aplicação</li>
                      </ul>
                    </div>
                  </div>

                  <button
                    onClick={() => handleComprar(pkg.name)}
                    className="btn-cta w-full flex items-center justify-center gap-2 text-sm font-black"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    Comprar via WhatsApp
                  </button>
                </motion.div>
              );
            })}
          </div>
        )}

        {!isLoading && packages.length === 0 && (
          <div className="text-center py-16">
            <Package className="w-16 h-16 text-luna_pink-200 mx-auto mb-4" />
            <p className="text-gray-500 font-medium">Nenhum pacote encontrado</p>
          </div>
        )}
      </div>
    </div>
  );
}
