'use client'

import { useCallback, useState } from 'react'
import type { ToastItem } from '@/components/Toast'

let nextId = 0

export function useToast() {
  const [toasts, setToasts] = useState<ToastItem[]>([])

  const show = useCallback((message: string, type: ToastItem['type'] = 'success') => {
    const id = ++nextId
    setToasts((prev) => [...prev, { id, message, type }])
  }, [])

  const close = useCallback((id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id))
  }, [])

  return { toasts, show, close }
}
