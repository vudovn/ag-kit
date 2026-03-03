"use client";

import { useState } from 'react'
import { motion } from 'framer-motion'

interface ToastProps {
    message: string
    type: 'success' | 'error' | 'info'
    onClose: () => void
}

export function Toast({ message, type, onClose }: ToastProps) {
    const colors = {
        success: 'bg-emerald-50 border-emerald-200 text-emerald-800',
        error: 'bg-red-50 border-red-200 text-red-800',
        info: 'bg-blue-50 border-blue-200 text-blue-800',
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: -20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.95 }}
            className={`fixed top-6 right-6 z-[100] px-5 py-3.5 rounded-2xl border shadow-lg backdrop-blur-sm ${colors[type]} max-w-sm`}
        >
            <div className="flex items-center gap-3">
                <span className="text-sm font-semibold">{message}</span>
                <button onClick={onClose} className="ml-2 opacity-60 hover:opacity-100 transition-opacity text-lg leading-none">×</button>
            </div>
        </motion.div>
    )
}
