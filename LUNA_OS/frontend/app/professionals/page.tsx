"use client";

import useSWR from 'swr';
import { motion } from 'framer-motion';
import { Users, Clock, Star, Scissors, ExternalLink, AlertCircle } from 'lucide-react';

const fetcher = (url: string) => fetch(url).then(res => res.json());

const WHATSAPP_NUMBER = '554991099437';

const AVATAR_GRADIENTS = [
  'from-luna_pink-400 to-luna_pink-600',
  'from-purple-400 to-indigo-500',
  'from-rose-400 to-pink-500',
  'from-fuchsia-400 to-purple-500',
  'from-pink-400 to-rose-500',
  'from-violet-400 to-purple-500',
];

function ProfessionalSkeleton() {
  return (
    <div className="card-md p-6 animate-pulse">
      <div className="flex items-start gap-4 mb-4">
        <div className="w-16 h-16 rounded-full bg-luna_pink-100" />
        <div className="flex-1 space-y-2">
          <div className="h-5 bg-luna_pink-100 rounded w-3/4" />
          <div className="h-3 bg-luna_pink-50 rounded w-1/2" />
        </div>
      </div>
      <div className="space-y-2">
        <div className="h-3 bg-luna_pink-50 rounded w-full" />
        <div className="h-3 bg-luna_pink-50 rounded w-2/3" />
      </div>
    </div>
  );
}

export default function ProfessionalsPage() {
  const { data, error, isLoading } = useSWR('/api/professionals', fetcher);

  if (error) return <div className="p-8 text-red-600">Erro ao carregar profissionais</div>;

  const professionals = data?.professionals || [];

  function handleAgendar(name: string) {
    const msg = encodeURIComponent(`Oi! Gostaria de agendar com ${name}`);
    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${msg}`, '_blank');
  }

  return (
    <div className="flex-1 overflow-y-auto bg-[var(--color-bg)] p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <p className="section-label mb-1">Catálogo Haven</p>
          <h1 className="text-3xl font-black text-gray-900 mb-2">Profissionais</h1>
          <p className="text-sm text-gray-500">Conheça nossa equipe de especialistas</p>
        </div>

        {isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => <ProfessionalSkeleton key={i} />)}
          </div>
        )}

        {!isLoading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {professionals.map((prof: any, index: number) => (
              <motion.div
                key={prof.key}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.07 }}
                className="card-md p-6 hover:shadow-card-lg transition-all group"
              >
                <div className="flex items-start gap-4 mb-5">
                  <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${AVATAR_GRADIENTS[index % AVATAR_GRADIENTS.length]} flex items-center justify-center text-white text-xl font-black flex-shrink-0 shadow-sm`}>
                    {prof.nickname?.[0] || prof.name[0]}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h2 className="text-lg font-black text-gray-900 truncate">{prof.name}</h2>
                    {prof.nickname && <p className="text-sm text-gray-500 font-medium">({prof.nickname})</p>}
                    <div className="flex items-center gap-1.5 mt-1.5">
                      <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                      <span className="text-xs font-bold text-gray-600 capitalize">{prof.level?.replace('_', ' ')}</span>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <div className="flex items-center gap-1.5 mb-1.5">
                      <Scissors className="w-3.5 h-3.5 text-luna_pink-500" />
                      <p className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Especialidades</p>
                    </div>
                    <div className="flex flex-wrap gap-1.5">
                      {prof.specialties?.map((s: string) => (
                        <span key={s} className="px-2 py-0.5 bg-luna_pink-50 text-luna_pink-700 text-[10px] font-bold rounded-full border border-luna_pink-100">{s}</span>
                      ))}
                    </div>
                  </div>

                  {prof.schedule && (
                    <div>
                      <div className="flex items-center gap-1.5 mb-1.5">
                        <Clock className="w-3.5 h-3.5 text-gray-400" />
                        <p className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Horários</p>
                      </div>
                      <div className="text-xs text-gray-600 space-y-0.5">
                        {Object.entries(prof.schedule).map(([day, schedule]) => (
                          <div key={day} className="flex justify-between">
                            <span className="capitalize text-gray-400">{day}</span>
                            <span className="font-semibold">{schedule as string}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {prof.alert && (
                    <div className="flex items-start gap-2 p-2.5 rounded-xl bg-amber-50 border border-amber-200">
                      <AlertCircle className="w-3.5 h-3.5 text-amber-500 mt-0.5 flex-shrink-0" />
                      <p className="text-[11px] text-amber-700 font-medium">{prof.alert}</p>
                    </div>
                  )}
                </div>

                <div className="mt-5 pt-4 border-t border-luna_pink-100">
                  <button
                    onClick={() => handleAgendar(prof.nickname || prof.name)}
                    className="btn-primary w-full flex items-center justify-center gap-2 text-sm"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    Agendar com {prof.nickname || prof.name}
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        )}

        {!isLoading && professionals.length === 0 && (
          <div className="text-center py-16">
            <Users className="w-16 h-16 text-luna_pink-200 mx-auto mb-4" />
            <p className="text-gray-500 font-medium">Nenhum profissional encontrado</p>
          </div>
        )}
      </div>
    </div>
  );
}
