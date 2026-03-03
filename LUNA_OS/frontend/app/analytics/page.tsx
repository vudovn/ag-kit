"use client";

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

/**
 * Analytics Redirect
 * Redireciona automaticamente para /analytics-super (versão completa)
 */
export default function AnalyticsRedirect() {
  const router = useRouter()

  useEffect(() => {
    router.push('/analytics-super')
  }, [router])

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="text-center">
        <p className="text-gray-500 font-medium mb-2">Redirecionando para Analytics PRO...</p>
        <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto" />
      </div>
    </div>
  )
}
