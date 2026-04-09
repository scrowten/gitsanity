'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Bookmark, Loader2 } from 'lucide-react'
import { NavBar } from '@/components/NavBar'
import { RepoCard } from '@/components/RepoCard'
import { RepoCardSkeleton } from '@/components/RepoCardSkeleton'
import { Toaster } from '@/components/Toast'
import { getSaved, repoAction } from '@/lib/api'
import { useAuth } from '@/lib/auth'
import { useToast } from '@/lib/useToast'

export default function SavedPage() {
  const router = useRouter()
  const { isAuthenticated, isLoading: authLoading } = useAuth()
  const queryClient = useQueryClient()
  const { toasts, show: showToast, close: closeToast } = useToast()

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/')
    }
  }, [authLoading, isAuthenticated, router])

  const { data, isLoading, isError } = useQuery({
    queryKey: ['saved'],
    queryFn: getSaved,
    enabled: isAuthenticated,
  })

  const unsaveMutation = useMutation({
    mutationFn: (id: number) => repoAction(id, 'dismissed'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saved'] })
      showToast('Removed from saved', 'info')
    },
    onError: () => showToast('Something went wrong — please try again', 'info'),
  })

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
      </div>
    )
  }

  if (!isAuthenticated) return null

  return (
    <>
      <NavBar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Saved Repos</h1>
          <p className="text-sm text-gray-500 mt-0.5">
            {data
              ? `${data.length} repo${data.length !== 1 ? 's' : ''} saved`
              : 'Your bookmarked repositories'}
          </p>
        </div>

        {/* Skeleton loading */}
        {isLoading && (
          <div className="grid grid-cols-1 gap-4">
            {Array.from({ length: 3 }).map((_, i) => (
              <RepoCardSkeleton key={i} />
            ))}
          </div>
        )}

        {isError && (
          <div className="text-center py-20 text-gray-500">
            Could not load saved repos.
          </div>
        )}

        {!isLoading && !isError && data?.length === 0 && (
          <div className="text-center py-20">
            <Bookmark className="w-10 h-10 text-gray-200 mx-auto mb-3" />
            <p className="text-gray-500 mb-1">No saved repos yet.</p>
            <p className="text-sm text-gray-400">
              Hit <strong>Save</strong> on repos from your feed to bookmark them here.
            </p>
          </div>
        )}

        {!isLoading && (
          <div className="grid grid-cols-1 gap-4">
            {data?.map((repo) => (
              <RepoCard
                key={repo.github_id}
                repo={repo}
                saved
                onUnsave={(id) => unsaveMutation.mutate(id)}
              />
            ))}
          </div>
        )}
      </div>

      <Toaster toasts={toasts} onClose={closeToast} />
    </>
  )
}
