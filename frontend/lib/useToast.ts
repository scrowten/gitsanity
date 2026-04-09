'use client'

import { useCallback, useState } from 'react'
import type { ToastItem } from '@/components/Toast'

// M-1: Use crypto.randomUUID() instead of a module-level mutable counter.
// The counter was shared across all hook instances and would produce duplicate
// IDs under concurrent renders or SSR.

export function useToast() {
  const [toasts, setToasts] = useState<ToastItem[]>([])

  const show = useCallback((message: string, type: ToastItem['type'] = 'success') => {
    const id = crypto.randomUUID()
    setToasts((prev) => [...prev, { id, message, type }])
  }, [])

  const close = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id))
  }, [])

  return { toasts, show, close }
}
