'use client'

import { useEffect } from 'react'
import { CheckCircle, X, Info } from 'lucide-react'

export interface ToastItem {
  id: number
  message: string
  type?: 'success' | 'info'
}

interface ToastProps {
  toast: ToastItem
  onClose: (id: number) => void
}

function Toast({ toast, onClose }: ToastProps) {
  useEffect(() => {
    const timer = setTimeout(() => onClose(toast.id), 3000)
    return () => clearTimeout(timer)
  }, [toast.id, onClose])

  const Icon = toast.type === 'info' ? Info : CheckCircle
  const iconClass = toast.type === 'info' ? 'text-blue-400' : 'text-green-400'

  return (
    <div className="flex items-center gap-2.5 px-4 py-3 bg-gray-900 text-white rounded-xl shadow-lg text-sm min-w-[220px] max-w-xs">
      <Icon className={`w-4 h-4 shrink-0 ${iconClass}`} />
      <span className="flex-1">{toast.message}</span>
      <button
        onClick={() => onClose(toast.id)}
        className="text-gray-400 hover:text-white transition-colors shrink-0"
        aria-label="Dismiss"
      >
        <X className="w-3.5 h-3.5" />
      </button>
    </div>
  )
}

interface ToasterProps {
  toasts: ToastItem[]
  onClose: (id: number) => void
}

export function Toaster({ toasts, onClose }: ToasterProps) {
  if (toasts.length === 0) return null
  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
      {toasts.map((t) => (
        <Toast key={t.id} toast={t} onClose={onClose} />
      ))}
    </div>
  )
}
