'use client'

import { useQuery } from '@tanstack/react-query'
import { getMe } from './api'
import type { User } from '@/types'

export function useAuth(): { user: User | null; isLoading: boolean; isAuthenticated: boolean } {
  const { data: user, isLoading } = useQuery({
    queryKey: ['auth', 'me'],
    queryFn: getMe,
    retry: false,
    staleTime: 5 * 60 * 1000,
  })

  return {
    user: user ?? null,
    isLoading,
    isAuthenticated: !!user,
  }
}
